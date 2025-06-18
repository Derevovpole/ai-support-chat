import json
import re
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from typing import Optional

# Загрузка .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY не найден. Убедитесь, что файл .env существует и содержит ключ.")
print("API KEY:", api_key)
client = OpenAI(api_key=api_key)

# Загрузка базы заказов
ORDERS_PATH = Path(__file__).parent / "orders.json"
with open(ORDERS_PATH, "r", encoding="utf-8") as f:
    orders = json.load(f)

# Извлечение номера заказа
def extract_order_number(message: str) -> Optional[str]:
    match = re.search(r"\b\d{5}\b", message)
    return match.group(0) if match else None

def detect_language(text: str) -> str:
    cyrillic_letters = sum(1 for ch in text if 'а' <= ch.lower() <= 'я')
    return 'ru' if cyrillic_letters > 3 else 'en'

def generate_response(message: str) -> str:
    message = message.lower()
    lang = detect_language(message)
    order_id = extract_order_number(message)

    # Фейковая база заказов
    if order_id and order_id in orders:
        order = orders[order_id]
        if lang == 'ru':
            return f"Заказ №{order_id}: {order['product']} — {order['status']}, оформлен {order['date']}."
        else:
            return f"Order #{order_id}: {order['product']} — {order['status']}, placed on {order['date']}."

    # Типовые вопросы (FAQ)
    faq_ru = {
        "доставка": "Доставка занимает 2-3 дня. Трек-номер отправляется на почту.",
        "возврат": "Вы можете вернуть товар в течение 14 дней. Подробнее на сайте.",
        "гарантия": "Гарантия на все товары — 12 месяцев.",
        "оплата": "Доступны карты, СБП, и оплата при получении.",
        "связь": "Наш оператор свяжется с вами в течение 15 минут.",
    }

    faq_en = {
        "delivery": "Delivery takes 2-3 days. Tracking number will be emailed to you.",
        "return": "You can return items within 14 days. See our return policy online.",
        "warranty": "All products have a 12-month warranty.",
        "payment": "We accept cards, Apple Pay, and bank transfers.",
        "contact": "Our operator will contact you within 15 minutes.",
    }

    # Подбор FAQ-ответа
    if lang == 'ru':
        for key, answer in faq_ru.items():
            if key in message:
                return answer
        return "Спасибо за сообщение! Уточните ваш вопрос или номер заказа."
    else:
        for key, answer in faq_en.items():
            if key in message:
                return answer
        return "Thank you! Please clarify your question or provide your order number."


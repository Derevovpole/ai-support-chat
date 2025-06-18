import os
import subprocess
from dotenv import load_dotenv

# Загрузим переменные из .env
load_dotenv()

# Получим ключ
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise RuntimeError("OPENAI_API_KEY не найден в .env файле!")

# Передаём переменные окружения вручную
env = os.environ.copy()
env["OPENAI_API_KEY"] = str(api_key)

# Запуск uvicorn
subprocess.run(
    ["uvicorn", "backend.main:app", "--reload"],
    env=env
)

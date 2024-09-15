
# Використовуємо базовий образ Python 3.12
FROM python:3.12-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл pyproject.toml та poetry.lock (якщо є) у робочу директорію
COPY pyproject.toml poetry.lock* ./

# Встановлюємо poetry
RUN pip install poetry

# Встановлюємо всі залежності
RUN poetry install --no-dev

# Копіюємо весь вміст поточної директорії у робочу директорію контейнера
COPY . .


# Вказуємо команду для запуску застосунку
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Відкриваємо порт
EXPOSE 8000
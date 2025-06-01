# 1. Берём облегчённую версию Python 3.13
FROM python:3.13-slim

# 2. Указываем рабочую папку внутри контейнера
WORKDIR /app

# 3. Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# 4. Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь остальной код проекта в контейнер
COPY . /app

# 6. Открываем порт 8000 (того же, который использует Uvicorn)
EXPOSE 8000

# 7. Команда, которая будет запущена при старте контейнера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

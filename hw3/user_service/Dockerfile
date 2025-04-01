# user_service/Dockerfile
FROM python:3.9-slim
# Устанавливаем нужные системные пакеты
RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

# Копируем requirements
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . /app

EXPOSE 8001
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
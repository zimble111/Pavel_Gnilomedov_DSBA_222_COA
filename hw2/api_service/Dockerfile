# api_service/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Копируем package.json и package-lock.json (если есть)
COPY package*.json /app/

# Устанавливаем зависимости
RUN npm install --omit=dev

# Копируем исходный код
COPY . /app

# Слушаем порт 8000 внутри контейнера
EXPOSE 8000

CMD ["npm", "start"]
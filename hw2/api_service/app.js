// api_service/app.js
const express = require('express');
const axios = require('axios');

const app = express();
app.use(express.json());

// URL нашего сервиса пользователей (контейнер user-service)
const USER_SERVICE_URL = 'http://user-service:8001';

// Универсальный роут для проксирования всех методов
app.all('*', async (req, res) => {
  try {
    const path = req.originalUrl;  // /api/v1/auth/register, /api/v1/users/profile, etc.
    const url = `${USER_SERVICE_URL}${path}`;

    // Формируем запрос к user_service
    const axiosConfig = {
      method: req.method,
      url: url,
      headers: {
        // Перенаправляем заголовки, кроме host
        ...req.headers,
        host: undefined
      },
      params: req.query,
      data: req.body
    };

    const response = await axios(axiosConfig);

    // Проксируем ответ обратно
    res.status(response.status).send(response.data);
  } catch (err) {
    if (err.response) {
      // Ошибка, пришедшая от user_service
      res.status(err.response.status).send(err.response.data);
    } else {
      // Иная ошибка (сетевые проблемы и т.д.)
      res.status(500).send({ error: err.message });
    }
  }
});

// Запуск приложения
const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
  console.log(`API Service (Proxy) listening on port ${PORT}`);
});
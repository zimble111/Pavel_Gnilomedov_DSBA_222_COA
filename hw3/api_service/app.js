const express = require('express');
const axios = require('axios');
const postsRouter = require('./routes/posts');

const app = express();
app.use(express.json());

const USER_SERVICE_URL = 'http://user-service:8001';

// REST → gRPC для постов
app.use('/api/v1/posts', postsRouter);

// Остальные маршруты — проксируем на user-service
app.all('*', async (req, res) => {
  try {
    const path = req.originalUrl;
    const url = `${USER_SERVICE_URL}${path}`;

    const axiosConfig = {
      method: req.method,
      url,
      headers: { ...req.headers, host: undefined },
      params: req.query,
      data: req.body,
    };

    const response = await axios(axiosConfig);
    res.status(response.status).send(response.data);
  } catch (err) {
    if (err.response) {
      res.status(err.response.status).send(err.response.data);
    } else {
      res.status(500).send({ error: err.message });
    }
  }
});

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => {
  console.log(`API Service (proxy) running on port ${PORT}`);
});

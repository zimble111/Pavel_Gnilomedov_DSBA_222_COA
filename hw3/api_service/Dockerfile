FROM node:20-slim

WORKDIR /app

COPY api_service/ ./

COPY post_service/posts.proto ./posts.proto

RUN npm install

CMD ["npm", "start"]

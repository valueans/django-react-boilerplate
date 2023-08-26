FROM node:16-alpine AS builder

WORKDIR /app

COPY ./frontend/package.json ./

RUN npm install

COPY ./frontend/ ./
RUN npm run build

RUN npm install webpack-cli webpack-node-externals npm-run-all nodemon

CMD ["npm","run","dev"]


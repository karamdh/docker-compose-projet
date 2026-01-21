FROM node:20-alpine

WORKDIR /app
COPY package.json .
RUN npm install

COPY public ./public
COPY src ./src

EXPOSE 3000
ENV HOST=0.0.0.0
CMD ["npm", "start"]

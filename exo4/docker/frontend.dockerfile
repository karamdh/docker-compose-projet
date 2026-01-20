FROM node:20-alpine

WORKDIR /app
COPY frontend/etc/package.json .
RUN npm install

# React expects public/index.html
RUN mkdir -p public
COPY frontend/etc/index.html ./public/index.html

COPY frontend/src ./src

EXPOSE 3000
ENV HOST=0.0.0.0
CMD ["npm", "start"]

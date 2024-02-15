FROM node as build

RUN npm install -g vite

WORKDIR /app
COPY package.json .
RUN npm install
COPY public ./public
COPY src ./src
COPY index.html .
COPY jsconfig.json .
COPY vite.config.js .
RUN vite build

FROM nginx
RUN apt-get update && \
    apt-get install -y certbot && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /www
RUN mkdir /www/certbot
COPY --from=build /app/dist /www
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY nginx/cert/app.watchtime.com.br-crt.pem /etc/nginx/ssl/
COPY nginx/cert/app.watchtime.com.br-key.pem /etc/nginx/ssl/



FROM node:lts-slim

WORKDIR /usr/src/web

COPY web/package.json .
COPY web/yarn.lock .

RUN yarn

COPY web/ .

EXPOSE 3000

CMD ["yarn", "dev"]

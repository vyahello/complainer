FROM node:17.4.0
LABEL version=0.1.0 \
      metadata="The main image for complainer frontend application part" \
      maintainer="Volodymyr Yahello <vyahello@gmail.com>"
ENV NODE_OPTIONS=--openssl-legacy-provider
WORKDIR /app
COPY fe .
RUN npm install -g @angular/cli
RUN npm install
CMD ng serve --host 0.0.0.0
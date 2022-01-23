FROM postgres:14.1-alpine
LABEL version=0.1.0 \
      metadata="The base image for complainer db application part" \
      maintainer="Volodymyr Yahello <vyahello@gmail.com>"
ARG POSTGRES_PASSWORD
ENV  POSTGRES_USER=postgres \
     POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
COPY docker/db/init.sql /docker-entrypoint-initdb.d/

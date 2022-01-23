FROM python:3.9.5-slim
LABEL version=0.1.0 \
      metadata="The base image for complainer backend application part" \
      maintainer="Volodymyr Yahello <vyahello@gmail.com>"
WORKDIR /app
COPY complainer complainer
COPY requirements.txt app.py .env ./
RUN pip install --no-cache-dir --upgrade pip && \
    apt-get update && \
    apt-get autoclean -y && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -v requirements.txt
ENTRYPOINT ["python", "app.py"]
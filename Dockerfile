FROM python:3.12-alpine

LABEL maintainer="@yry0008"
LABEL description="A simple web server that forwards requests to Alibaba Cloud, avoid signature verification on the client side."
LABEL version="1.0.0"

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT [ "python", "main.py" ]
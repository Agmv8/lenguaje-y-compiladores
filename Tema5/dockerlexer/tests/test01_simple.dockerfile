FROM ubuntu:20.04
LABEL maintainer="arnaldo@example.com"
ENV APP_HOME=/app
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y python3
EXPOSE 8080
CMD ["python3", "app.py"]

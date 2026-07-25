FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

LABEL maintainer="arnaldo@example.com"
LABEL description="Imagen de prueba extensa para benchmarking"
LABEL version="1.0.0"

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    net-tools \
    iputils-ping \
    ca-certificates \
    software-properties-common \
    python3 \
    python3-pip \
    python3-venv \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV APP_ENV=production
ENV APP_PORT=8000
ENV APP_HOST=0.0.0.0
ENV LOG_LEVEL=info

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY scripts/ ./scripts/
RUN chmod +x ./scripts/*.sh

COPY src/ ./src/
COPY config/ ./config/
COPY migrations/ ./migrations/

RUN python3 ./scripts/compile_assets.py

ARG BUILD_NUMBER=unknown
ENV BUILD_NUMBER=${BUILD_NUMBER}

VOLUME ["/opt/app/data"]
VOLUME ["/opt/app/logs"]

EXPOSE 8000
EXPOSE 8001
EXPOSE 9000

USER 1000

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=15s --timeout=3s --retries=3 CMD ["curl", "-f", "http://localhost:8000/health"]

ENTRYPOINT ["python3", "./scripts/entrypoint.py"]
CMD ["--workers", "4", "--port", "8000"]

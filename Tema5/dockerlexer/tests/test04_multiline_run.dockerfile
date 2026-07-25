FROM ubuntu:22.04

LABEL maintainer="arnaldo@example.com"
LABEL version="1.0"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git \
        build-essential \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/build

COPY . /opt/build

RUN make all && \
    make install && \
    make clean

VOLUME ["/data"]

STOPSIGNAL SIGTERM

CMD ["/opt/build/bin/start"]

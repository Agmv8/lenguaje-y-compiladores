# Etapa 1: build
FROM golang:1.21 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/app ./cmd/app

# Etapa 2: runtime
FROM alpine:3.19 AS runtime
RUN apk add --no-cache ca-certificates tzdata
WORKDIR /app
COPY --from=builder /out/app /app/app
COPY config/prod.yaml /app/config.yaml
ENV TZ=America/Caracas
ENV CONFIG_PATH=/app/config.yaml
LABEL org.opencontainers.image.source="https://github.com/example/app"
LABEL org.opencontainers.image.version="2.3.1"
USER 65532
EXPOSE 8080
EXPOSE 9090
HEALTHCHECK --interval=30s --timeout=5s CMD ["/app/app", "healthcheck"]
ENTRYPOINT ["/app/app"]
CMD ["--config", "/app/config.yaml"]

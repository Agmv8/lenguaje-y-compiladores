FROM redis:7.2-alpine
RUN mkdir -p /data
VOLUME /data
EXPOSE 6379
HEALTHCHECK CMD redis-cli ping || exit 1
CMD redis-server --appendonly yes

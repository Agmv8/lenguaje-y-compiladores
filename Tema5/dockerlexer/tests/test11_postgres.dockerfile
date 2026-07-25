FROM postgres:16-alpine
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_DB=appdb
COPY init.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
VOLUME /var/lib/postgresql/data

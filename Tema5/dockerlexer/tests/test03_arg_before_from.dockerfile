ARG VERSION=3.11
FROM python:${VERSION}-slim
ARG APP_ENV=production
ENV APP_ENV=${APP_ENV}
WORKDIR /srv/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER 1000
EXPOSE 5000
ENTRYPOINT ["python", "manage.py", "runserver"]

FROM python:3-alpine

ENV APP_REFRESH 10
ENV APP_CONFIG "/usr/src/app/config.d"
ENV TRAEFIK_URL "https://127.0.0.1:8080"
ENV TRAEFIK_USER ""
ENV TRAEFIK_PASS ""
ENV TRAEFIK_ENTRYPOINT "*"
ENV TRAEFIK_ENTRYPOINTS "http,https"

WORKDIR /usr/src/app
COPY server.py ./
COPY requirements.txt ./
COPY App ./App

VOLUME /usr/src/app/config.d
RUN pip install -r requirements.txt

CMD ["python", "server.py"]

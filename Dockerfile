FROM python:3-alpine

ENV APP_REFRESH 10
ENV APP_CONFIG "/usr/src/app/config.d"
ENV TRAEFIK_URL "https://127.0.0.1:8080"
ENV TRAEFIK_USER ""
ENV TRAEFIK_PASS ""

WORKDIR /usr/src/app
COPY App .
COPY requirements.txt .
COPY server.py .

VOLUME /usr/src/app/config.d
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "server.py"]
CMD [""]
FROM python:alpine

ENV DB_URI "mysql+pymysql://root:test@mariadb/tmm"
ENV REFRESH_RATE 60

ENV PANEL_PORT 5000
ENV PANEL_HOST "0.0.0.0"
ENV PANEL_SECRET "abcdefghijklmnopqrstuvwxyz"

ENV TRAEFIK_URL "http://traefik:8080"
ENV TRAEFIK_USER ""
ENV TRAEFIK_PASS ""

WORKDIR /usr/src/app
COPY requirements.txt .
COPY server.py .
COPY App .

RUN pip install -r requirements.txt
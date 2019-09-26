FROM python:3-alpine

ENV MESH_REFRESH 10
ENV MESH_CONFIG "/config"
ENV MESH_TRAEFIK_URL "http://127.0.0.1:8080"
ENV MESH_TRAEFIK_USER ""
ENV MESH_TRAEFIK_PASS ""
ENV MESH_TRAEFIK_ENTRYFILTER "*"
ENV MESH_TRAEFIK_ENTRYPOINTS "http,https"

WORKDIR /usr/src/app
COPY server.py ./
COPY requirements.txt ./
COPY App ./App

VOLUME /config
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "server.py"]

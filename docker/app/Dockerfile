FROM python:3.10-slim

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache \
(  apt update && apt install build-essential gcc -y && apt update \
)

COPY docker/app/requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

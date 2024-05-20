FROM python:3.11.2-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /opt/app

RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y build-essential git \
    && apt-get install -y libpq-dev \
    && apt-get install -y python3-apt \
    && apt-get install -y python3-distutils \
    && apt-get install -y python3-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ ./src
COPY start.sh start.sh
RUN chmod +x start.sh

EXPOSE 8080

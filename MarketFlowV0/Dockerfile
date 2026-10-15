FROM python:3.13.7-slim-trixie
RUN apt-get update && apt-get install -y --no-install-recommends default-jre-headless \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /workspace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV JAVA_HOME=/usr/lib/jvm/default-java PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

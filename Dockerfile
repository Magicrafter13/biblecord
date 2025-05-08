# syntax=docker/dockerfile:1

FROM python:3.12

LABEL org.opencontainers.image.title="BibleCord Discord Bot"
LABEL org.opencontainers.image.description="Yet Another Discord Bot for Bible Verses"
LABEL org.opencontainers.image.authors="self@matthewrease.net"

# Files

WORKDIR /app

## Python Packages

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

## Main Files

COPY bot.py .

# Runtime

ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python3", "bot.py"]

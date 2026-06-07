# syntax=docker/dockerfile:1

# === BUILD STAGE ===

FROM dhi.io/python:3.12-dev AS builder

## Python Packages

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

# === RUNTIME STAGE ===

FROM dhi.io/python:3.12

LABEL org.opencontainers.image.title="BibleCord Discord Bot"
LABEL org.opencontainers.image.description="Yet Another Discord Bot for Bible Verses"
LABEL org.opencontainers.image.authors="self@matthewrease.net"

# Package Files

COPY --from=builder /opt/python /opt/python

# App Files

WORKDIR /app
USER nonroot
COPY bot.py .

# Runtime

ENV PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT ["python"]
CMD ["bot.py"]

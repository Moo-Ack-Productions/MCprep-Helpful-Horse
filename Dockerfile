# syntax=docker/dockerfile:1.2

# Download packages
FROM python:3.10-slim as builder

WORKDIR /app

# Update
RUN pip install -U \
    pip \
    setuptools \
    wheel

COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# FINAL IMAGE
FROM python:3.10-slim

# Tini
ENV TINI_VERSION="v0.19.0"
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

WORKDIR /app
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Update stuff
RUN pip install -U \
    pip \
    setuptools \
    wheel

# Create user so process doesn't run as root
RUN addgroup --system app && adduser --system --group app
USER app

# Install wheels, copy the files, and start running
RUN pip install --upgrade pip && pip install --no-cache /wheels/*
COPY . .

ENTRYPOINT ["/tini", "--"]
CMD [ "python3", "main.py"]

# syntax=docker/dockerfile:1.2

# This image sets up packages and whatnot, it will not be 
# included in the final image
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .

# Update
RUN pip install -U \
    pip \
    setuptools \
    wheel \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# FINAL IMAGE
FROM python:3.10-slim

# Tini
ENV TINI_VERSION="v0.19.0"

# Remove arm64 at the end if you don't use ARM, Helpful Horse runs on an ARM
# server as of now
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-arm64 /tini
RUN chmod +x /tini

# Workdir and copying stuff from the builder image
WORKDIR /app
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Update stuff and create new user
RUN pip install -U \
    pip \
    setuptools \
    wheel \
    && addgroup --system app && adduser --system --group app

# Change user
USER app

# Install wheels, copy the files, and start running
RUN pip install --upgrade pip && pip install --no-cache /wheels/*
COPY . .

ENTRYPOINT ["/tini", "--"]
CMD [ "python3", "main.py"]

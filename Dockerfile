# syntax=docker/dockerfile:1.2

# This image sets up packages and whatnot, it will not be 
# included in the final image
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .

# Update
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U \
    pip \
    setuptools \
    wheel \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# FINAL IMAGE
FROM python:3.10-slim

# Workdir and copying stuff from the builder image
WORKDIR /app
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Update stuff, create new user, and install packages
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install -U \
    pip \
    setuptools \
    wheel \
    && addgroup --system app \
    && adduser --no-create-home --system --group app \
    && pip install --no-cache /wheels/*

# Change user so that commands don't run as root
USER app

COPY . .
CMD [ "python3", "main.py"]

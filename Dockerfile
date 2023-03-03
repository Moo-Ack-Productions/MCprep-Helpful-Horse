# syntax=docker/dockerfile:1.2

# Set up environment
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# What's actually in the final image
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Create user so process doesn't run as root
RUN addgroup --system app && adduser --system --group app
USER app

# Install wheels, copy the files, and start running
RUN pip3 install --upgrade pip && pip install --no-cache /wheels/*
COPY . .
CMD [ "python3", "main.py"]

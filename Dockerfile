FROM python:3.11-slim

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PORT=5000

# Install system dependencies + Chromium + required libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev build-essential \
        wget curl gnupg2 ca-certificates \
        fonts-liberation \
        chromium chromium-driver \
        libnss3 libxss1 libasound2 libatk-bridge2.0-0 \
        libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
        libxrandr2 xdg-utils && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Make sure Chrome/Chromium uses the right path
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Run Flask app with Gunicorn (shell form for $PORT expansion)
CMD gunicorn -w 1 -k gevent -t 120 -b 0.0.0.0:$PORT app:app

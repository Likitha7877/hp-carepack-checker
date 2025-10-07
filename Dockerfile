FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PORT=5000

# Install system dependencies and Chrome dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget curl gnupg2 ca-certificates fonts-liberation \
        libnss3 libxss1 libasound2 libatk-bridge2.0-0 \
        libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
        libxrandr2 xdg-utils build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Run Flask app with Gunicorn (shell form for $PORT expansion)
CMD gunicorn -w 1 -k gevent -t 120 -b 0.0.0.0:$PORT app:app

FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
       wget curl gnupg2 ca-certificates fonts-liberation \
       libnss3 libxss1 libasound2 libatk-bridge2.0-0 \
       libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
       libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
       libxrandr2 xdg-utils xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Chromium and ChromeDriver
RUN apt-get update && apt-get install -y chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome path
ENV CHROME_BIN=/usr/bin/chromium

WORKDIR /app
COPY . .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

CMD ["sh", "-c", "xvfb-run -a gunicorn -w 1 -k gevent -t 120 -b 0.0.0.0:${PORT:-5000} app:app"]

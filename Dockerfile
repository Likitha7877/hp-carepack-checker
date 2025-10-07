FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PORT=5000
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install dependencies + Chromium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev build-essential \
        wget curl unzip ca-certificates fonts-liberation \
        libnss3 libxss1 libasound2 libatk-bridge2.0-0 \
        libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
        libxrandr2 xdg-utils chromium && \
    rm -rf /var/lib/apt/lists/*

# Download matching ChromeDriver
RUN CHROME_VERSION=$(chromium --version | grep -oP '\d+\.\d+\.\d+') && \
    MAJOR_VERSION=${CHROME_VERSION%%.*} && \
    echo "Chromium version: $CHROME_VERSION, major: $MAJOR_VERSION" && \
    DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$MAJOR_VERSION") && \
    echo "Matching ChromeDriver version: $DRIVER_VERSION" && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/bin/ && \
    chmod +x /usr/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Set working directory
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run Flask app with Gunicorn
CMD gunicorn -w 1 -k gevent -t 120 -b 0.0.0.0:$PORT app:app

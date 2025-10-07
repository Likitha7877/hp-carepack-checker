FROM python:3.11-slim

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PORT=5000
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install minimal dependencies + Chromium + unzip + curl
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev build-essential \
        wget curl unzip ca-certificates fonts-liberation \
        chromium \
        libnss3 libxss1 libasound2 libatk-bridge2.0-0 \
        libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
        libxrandr2 xdg-utils && \
    rm -rf /var/lib/apt/lists/*

# Get Chromium version and download matching ChromeDriver
RUN CHROME_VERSION=$(chromium --version | awk '{print $2}') && \
    MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) && \
    DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$MAJOR_VERSION") && \
    echo "Chromium: $CHROME_VERSION, ChromeDriver: $DRIVER_VERSION" && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/bin/ && \
    chmod +x /usr/bin/chromedriver && \
    rm /tmp/chromedriver.zip

# Set working directory and copy app
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run Flask app with Gunicorn
CMD gunicorn -w 1 -k gevent -t 120 -b 0.0.0.0:$PORT app:app

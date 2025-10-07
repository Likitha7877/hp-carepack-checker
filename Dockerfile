FROM python:3.11-slim

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV PORT=5000
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Install dependencies + Chromium + unzip + libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
        bash curl wget unzip chromium \
        libnss3 libxss1 libasound2 libatk-bridge2.0-0 \
        libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
        libxrandr2 xdg-utils fonts-liberation python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver matching Chromium version
RUN bash -c '\
    CHROME_VERSION=$(chromium --version | grep -o "[0-9]*\.[0-9]*\.[0-9]*") && \
    CHROME_MAJOR=$(echo $CHROME_VERSION | cut -d"." -f1) && \
    CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/bin/ && \
    chmod +x /usr/bin/chromedriver && \
    rm /tmp/chromedriver.zip'

# Set working directory
WORKDIR /app
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Run Flask app with Gunicorn
CMD gunicorn -w 1 -k gevent -t 120 -b 0.0.0.0:$PORT app:app

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 ca-certificates fonts-liberation \
    libnss3 libxss1 libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 xdg-utils xvfb && \
    apt-get clean

# Add Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean

# Set environment variable for virtual display
ENV DISPLAY=:99

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD xvfb-run --server-args="-screen 0 1024x768x24" gunicorn --bind 0.0.0.0:${PORT:-10000} app:app

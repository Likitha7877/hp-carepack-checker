FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg2 ca-certificates fonts-liberation \
    libnss3 libxss1 libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 xdg-utils xvfb && \
    apt-get clean

# ✅ Install Google Chrome
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean

# ✅ Install matching ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION} || echo "latest") && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Set environment variable for virtual display
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Start Flask app with gunicorn and xvfb
CMD xvfb-run --server-args="-screen 0 1024x768x24" gunicorn --bind 0.0.0.0:${PORT:-10000} app:app

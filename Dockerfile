FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl unzip wget gnupg2 fonts-liberation \
    libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils \
    xvfb chromium chromium-driver && \
    apt-get clean

# Set environment variables
ENV DISPLAY=:99

# Set work directory
WORKDIR /app

# Copy app files
COPY . .

# Install Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run the app with Xvfb
CMD xvfb-run --server-args="-screen 0 1024x768x24" gunicorn --bind 0.0.0.0:${PORT:-10000} app:app


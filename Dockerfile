# Use Python base image
FROM python:3.11-slim

# Install Chromium and ChromeDriver
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    wget \
    curl \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome and ChromeDriver
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy all files to the container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask/gunicorn will run on
EXPOSE 10000

# Start the app using Gunicorn (production-ready WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]

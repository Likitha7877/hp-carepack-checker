FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    xvfb \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome paths
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Copy app files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask/gunicorn will use
EXPOSE 10000

# Start the app with gunicorn inside a virtual display (xvfb-run)
CMD ["xvfb-run", "-a", "gunicorn", "-b", "0.0.0.0:10000", "app:app"]

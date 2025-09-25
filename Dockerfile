FROM python:3.11-slim

# Install system deps + Chrome + matching ChromeDriver
RUN apt-get update && apt-get install -y --no-install-recommends \
       wget unzip curl gnupg2 ca-certificates fonts-liberation \
       libnss3 libxss1 libappindicator3-1 libasound2 libatk-bridge2.0-0 \
       libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
       libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
       libxrandr2 xdg-utils \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d'.' -f1) \
    && DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") \
    && wget -q "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip -d /usr/local/bin/ \
    && rm chromedriver_linux64.zip \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/google-chrome-stable
ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /app
COPY . .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

CMD ["gunicorn", "-w", "1", "-k", "gevent", "-t", "120", "-b", "0.0.0.0:5000", "app:app"]

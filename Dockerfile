FROM python:3.11-slim

# Install system deps + Chrome
RUN apt-get update \
  && apt-get install -y \
       wget unzip curl gnupg2 ca-certificates fonts-liberation \
       libnss3 libxss1 libappindicator3-1 libasound2 libatk-bridge2.0-0 \
       libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
       libnspr4 libx11-xcb1 libxcomposite1 libxdamage1 \
       libxrandr2 xdg-utils xvfb chromium-driver \
  && rm -rf /var/lib/apt/lists/*

# Install Google Chrome stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
     | apt-key add - \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
     > /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update \
  && apt-get install -y google-chrome-stable \
  && rm -rf /var/lib/apt/lists/*

# Point Selenium at Chrome
ENV CHROME_BIN=/usr/bin/google-chrome-stable

WORKDIR /app
COPY . .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Launch under virtual X server
CMD ["sh", "-c", "xvfb-run -a gunicorn -w 1 -k gevent -t 120 -b 0.0.0.0:${PORT:-5000} app:app"]
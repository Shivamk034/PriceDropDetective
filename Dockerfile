# FROM python:slim AS app

# # We don't need the standalone Chromium
# ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
# ENV CHROME_BIN=/usr/bin/google-chrome

# # Install Google Chrome Stable and fonts
# # Note: this installs the necessary libs to make the browser work with Puppeteer.
# RUN apt-get update && apt-get install curl gnupg -y \
#   && curl --location --silent https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#   && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
#   && apt-get update \
#   && apt-get install google-chrome-stable -y --no-install-recommends \
#   && rm -rf /var/lib/apt/lists/*

# COPY . /app
# WORKDIR /app

# RUN ls -lh

# RUN pip3 install -r requirements.txt --no-cache-dir

# RUN chmod 777 /app;
# RUN chmod 777 startup.sh
# RUN mkdir -p /.cache/selenium
# RUN chmod 777 /.cache/selenium

# EXPOSE 8000

# CMD exec /app/startup.sh

FROM python:3.11-alpine


RUN addgroup webdriver && adduser -h /home/webdriver -s /bin/sh -G webdriver -D webdriver

WORKDIR /home/webdriver

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk update && apk add chromium-chromedriver chromium
ENV PATH="/usr/lib/chromium/:${PATH}"
RUN ln -s /usr/lib/chromium/chromium-launcher.sh /usr/local/bin/chrome

COPY . /app
WORKDIR /app

RUN ls -lh


RUN pip3 install -r requirements.txt --no-cache-dir

RUN touch db.sqlite3

RUN chmod 777 /app;
RUN chmod 777 db.sqlite3
RUN chmod 777 startup.sh

EXPOSE 8000


CMD exec /app/startup.sh

# https://huggingface.co/spaces/shivam-kala/Price-Drop-Detective
# https://shivam-kala-price-drop-detective.hf.space/
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


CMD /app/startup.sh

# https://huggingface.co/spaces/shivam-kala/Price-Drop-Detective
# https://shivam-kala-price-drop-detective.hf.space/


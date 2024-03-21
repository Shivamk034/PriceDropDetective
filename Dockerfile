FROM python:3.11-alpine


RUN addgroup webdriver && adduser -h /home/webdriver -s /bin/sh -G webdriver -D webdriver

WORKDIR /home/webdriver

RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk update && apk add chromium-chromedriver chromium
ENV PATH="/usr/lib/chromium/:${PATH}"
RUN ln -s /usr/lib/chromium/chromium-launcher.sh /usr/local/bin/chrome

# virtual display
RUN apk add xvfb

# RUN apk add imagemagick
# RUN mkdir /app/logs/ && mkdir /app/logs/images/
# RUN import -display :99 -window root /app/logs/images/screenshot.png
# RUN xwd -display :99 -root -silent | convert xwd:- png:/app/logs/images/screenshot.png

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
# apk add imagemagick
# import -display :99 -window root screenshot.png
# -display :99: Specifies the display to capture the screenshot from. In this case, it's using display :99.
# -window root: Specifies to capture the entire screen.
# screenshot.png: Specifies the filename to save the screenshot to. You can change it as needed.

FROM python:3.11-alpine


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
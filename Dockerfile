FROM python:alpine

COPY . /app
WORKDIR /app

RUN ls -lh

RUN pip3 install -r requirements.txt --no-cache-dir

RUN chmod 777 /app;
RUN chmod 777 startup.sh

EXPOSE 8000

CMD exec /app/startup.sh
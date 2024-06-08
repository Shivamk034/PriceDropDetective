FROM python:slim AS app

COPY . /app
WORKDIR /app

RUN ls -lh

RUN apt-get update && \
    apt-get install -y --no-install-recommends\
    git \
    git-lfs

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /app
RUN mkdir -p /etc/sudoers.d/
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

RUN pip3 install -r requirements.txt --no-cache-dir

RUN chmod 777 /app;
RUN chmod 777 on_startup.sh
RUN chmod 777 start_server.sh

EXPOSE 8000

CMD exec /app/on_startup.sh
# CMD echo "hello"
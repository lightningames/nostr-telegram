# TODO: add mongodb install and setup with the dbtools.py file
FROM python:3.9

RUN apt-get update && apt-get install -y mongodb
RUN mkdir -p /data/db
RUN echo 'dbpath = /data/db' >> /etc/mongodb.conf

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# set environment variables

# Setup database with dbtools
RUN python ./dbtools.py

CMD [ "python", "./tgbot.py" ]

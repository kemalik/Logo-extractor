FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD requirements.txt /app/

RUN mkdir /app/logs/

RUN pip install -r /app/requirements.txt

ADD . /app/

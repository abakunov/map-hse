FROM python:3.10-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . . 
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN python3 manage.py collectstatic --noinput
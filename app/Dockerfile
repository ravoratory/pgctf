FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y postgresql netcat
RUN pip install --upgrade pip

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

# RUN python manage.py collectstatic --noinput

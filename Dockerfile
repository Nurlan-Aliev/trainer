FROM python:3.13

WORKDIR /myapp

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /myapp/requirements.txt

COPY . .

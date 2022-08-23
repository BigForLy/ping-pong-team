FROM python:3.10.5

WORKDIR /usr/src/mic_1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/mic_1/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/mic_1/

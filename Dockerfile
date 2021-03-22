FROM python:3.8

COPY ./requirements.txt /setup/

WORKDIR /setup
RUN pip install -r requirements.txt

RUN mkdir /proj
WORKDIR /proj

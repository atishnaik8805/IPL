FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /ipl
WORKDIR /ipl
COPY . /ipl/
RUN pip install -r requirements.txt

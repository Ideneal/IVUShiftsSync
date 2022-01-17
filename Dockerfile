FROM python:3.9.1
RUN apt update
ADD . /ivu
WORKDIR /ivu
RUN pip install -r requirements.txt

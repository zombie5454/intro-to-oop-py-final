FROM ubuntu:22.04

WORKDIR /app

RUN apt update -y && apt upgrade -y

RUN apt install -y python3-pip

RUN apt install -y build-essential libssl-dev libffi-dev python3-dev

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
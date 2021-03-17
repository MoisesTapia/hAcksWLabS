FROM python:3.7.10-slim

LABEL NAME="hAckWsLabS"
LABEL MAINTAINER="Equinockx moisestapia741@gmail.com"
LABEL VERSION="1.0.0"

WORKDIR /home/

RUN mkdir .aws/

RUN cd .aws/ && \
    touch credentials config
COPY requirements.txt .

RUN apt-get update && \
    pip3 install -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
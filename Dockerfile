FROM python:3.7.10-slim

LABEL NAME="hAckWsLabS"
LABEL MAINTAINER="Equinockx moisestapia741@gmail.com"
LABEL VERSION="0.1.0"

WORKDIR /root
RUN mkdir .aws/
# Credentials Configuration 
RUN cd .aws && \
    touch credentials config && \
    echo "[default]" > config && \
    echo "region=us-east-1" >> config


WORKDIR /home/

COPY requirements.txt .
COPY hackslabs.py .


RUN apt-get update && \
    pip3 install -r requirements.txt && \
    chmod +x hackslabs.py && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "/bin/bash"]
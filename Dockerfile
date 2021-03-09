FROM python:3.7.9-slim-buster

LABEL NAME="hAckWsLabS"
LABEL MAINTAINER="Equinockx moisestapia741@gmail.com"
LABEL VERSION="1.0.0"

WORKDIR /home/

RUN mkdir .aws/

RUN cd .aws/ && \
    touch credentials config

RUN apt-get update && \
    pip3 install boto3 && \
    pip install argparse && \
    pip3 install awscli && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
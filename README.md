# hAcksWLabS

## Tools do you need

- [X] awscli
- [X] boto3
- [X] argparse

## How to use

```bash
➜  hAckWsLabS ✗ python3 awsinstance.py --help
usage: awsinstance.py [-h] [--awstype SIZE] [--maxvm MAXVM] [--minvm MINVM]
                      [--keypair KEYS] [--launch LAUNCH] [--stop STOP]
                      [--start START] [--terminate TERMINATE]
                      [--restart RESTART]
```
## Commands to use this script

|  short   |     large     |  help |
|----------|:-------------:|------:|
|    -z    |   --awstype   | $1600 |
|   -mx    |   --maxvm     |   $12 |
|   -mn    |   --minvm     |    $1 |
|   -k     |   --keypair   |    $1 |
|   -l     |   --launch    |    $1 |
|          |   --stop      |    $1 |
|   -s     |   --start     |    $1 |
|   -t     |   --terminate |    $1 |
|   -r     |   --restart   |    $1 |



## Use docker to deploy this tool

```bash
docker build -t hackslabs:1.0.0
```
## Run the docker container

```bash
docker run -d -ti --name hackslabs <image_id>
```

## verify that container is running

```bash
docker ps
```

```bash

```
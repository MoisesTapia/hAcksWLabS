# hAcksWLabS

https://www.travis-ci.com/MoisesTapia/hAcksWLabS.svg?token=5ExeHzDK51pVeE5oa7h7&branch=main

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
## Example
```bash
python3 hackslabs.py -l aws -z t2.micro -mx 1 -mn 1 -k KaliLinux
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

## [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/?nc1=h_ls)

|  Instance   |     vCPU*     |  CPU Credits / hour | Mem GiB|  Storage  | Network Performance |
|-------------|:-------------:|---------------------|:------:|-----------|:-------------------:|
|  t2.nano    |       1       |           3         |   0.5  |  EBS-Only |           Low       |
|  t2.micro   |       1       |           6         |    1   |  EBS-Only |   Low to Moderate   |
|  t2.small   |       1       |           12        |    2   |  EBS-Only |   Low to Moderate   |
|  t2.medium  |       2       |           24        |    4   |  EBS-Only |   Low to Moderate   |
|  t2.large   |       2       |           36        |    8   |  EBS-Only |   Low to Moderate   |
|  t2.xlarge  |       4       |           54        |    16  |  EBS-Only |      Moderate       |
|  t2.medium  |       8       |           81        |    32  |  EBS-Only |      Moderate       |


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
## Execute commands inside of container

```bash
docker exec -ti <conatiner_name> /bin/bash
```
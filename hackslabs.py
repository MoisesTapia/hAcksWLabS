#!/bin/env python
# Author: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
#

import boto3 as b3
import argparse as argp
from art import *
from colorama import Fore, init, Back, Style
import sys

VERDE = Fore.LIGHTGREEN_EX
RRED = Fore.LIGHTRED_EX
CYYAN = RRED =Fore.LIGHTCYAN_EX
RESETT = Fore.RESET

#
# ami-050184d2d97a1193f us-west-1
# ami-0671b2fb0bfa2a568 us-east-2
# https://github.com/infoslack/awesome-web-hacking
#

client = b3.client('ec2')



parser = argp.ArgumentParser(
    description=__doc__, 
    formatter_class=argp.RawDescriptionHelpFormatter)

parser.add_argument("-z", "--awstype", dest="size", 
                    help="""choose the sice of your vm in aws, types: 
                    t2.micro, t2.small, t2.medium, t2.large, t2.xlarge.
                    Remember visit aws.com to see the cost for each vm""")

parser.add_argument("-mx", "--maxvm", dest="maxvm",
                    help="Max number of the same instances",
                    type=int)

parser.add_argument("-mn", "--minvm", dest="minvm",
                    help="Min number of the same instances default 1",
                    default=1,
                    type=int)

parser.add_argument( "-k", "--keypair", dest="keys",
                    default='KaliLinux',
                    help="Name of your Key Pair in AWS (ssh keys)")

parser.add_argument("-l", "--launch",dest="launch",
                    default="aws",
                    help="""
                    This option requires the next attr:
                         --awstype, --maxvm, --minvm, --keypair
                    """)

parser.add_argument("--stop", dest="stop",
                    help="Stop the instance or instances")
parser.add_argument("-s", "--start", dest="start",
                    help="Start the instance or instances")
parser.add_argument("-t", "--terminate",dest="terminate",
                    type=str,
                    help="""
                    Terminate the instance or instances this option will delete the instances take care""")

parser.add_argument("-ls", "--list", dest="list",
                    type=str,
                    default="vms",
                    help="list all instances in your account")
parser.add_argument("-in" , "--getinfo", dest="getinfo",
                    type=str,
                    default="vm",
                    help="get info of your instance")


class Instance:
    """
    In this class we define the basic functions of EC2 instances like:
                - Launch
                - start
                - stop
                - terminate
    other options 
    """

    def __init__(self, imageid, instancetype, maxcount, mincount, keypair):

        self.imageid        =   imageid
        self.instancetype   =   instancetype
        self.mincount       =   mincount
        self.maxcount       =   maxcount
        self.keypair        =   keypair
    
    def runinstance(self):
        resp = client.run_instances(
            ImageId = self.imageid,
            InstanceType = self.instancetype,
            MinCount = self.mincount,
            MaxCount = self.maxcount,
            KeyName= self.keypair,
            TagSpecifications= [
                
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Purpose',
                            'Value': 'Pentesting Lab',
                            'Key' : 'Name',
                            'Value' : 'Kali Linux'
                        },
                    ],
                },
            ],
            
            )
        print("\tInstance DI\t\tImage ID\t\tDate\t\t\tKey Name\tPrivate IP")
        print("\t-----------\t\t--------\t----------------------\t\t-------\t\t----------")
        for info in resp['Instances']:
            print(info['InstanceId'] + "\t" + 
                  info['ImageId'] + "\t" + 
                  str(info['LaunchTime']) + "\t" + 
                  info['KeyName'] + "\t" + 
                  info['PrivateIpAddress'] )
            
        return resp
    
    def start_instances(self, instanceid):
        self.instanceid = instanceid 
        print("The next instance will be available in a few minutes")
        aws_start = client.start_instances(InstanceIds=[self.instanceid])
        
        for instances in aws_start['StartingInstances']:
            print("Instance ID: {}".format(instances['InstanceId']))
            print("Code ID: {}".format(instances['CurrentState']['Code']))
            print("State ID: {}".format(instances['CurrentState']['Name']))
        
    def stop_instances(self,instanceid):
        self.instanceid = instanceid
        print("The next instance will be stop for few seconds: {}".format(self.instanceid))
        
        aws_stop = client.stop_instances(InstanceIds=[self.instanceid])
        
        for instances in aws_stop['StoppingInstances']:
            print("Stop instance ID: {}".format(instances['InstanceId']))
            print("Code: {}".format(instances['CurrentState']['Code']))
            print("Code: {}".format(instances['CurrentState']['Name']))
            
    def terminate_instances(self,instanceid):
        self.instanceid = instanceid
        aws_terminate = client.terminate_instances(InstanceIds=[self.instanceid])
        
        for instances in aws_terminate['TerminatingInstances']:
            print("Stopping instance ID: " + RRED + instances['InstanceId'] + RESETT)
            print("Code: {}".format(instances['CurrentState']['Code']))
            print("Status: " + CYYAN + instances['CurrentState']['Name'] + RESETT)
    
    def getinfo_instances(self):
        resp = client.describe_instances()
        
        tprint('Resume')
        
        print(CYYAN + "\n\t\tList of Instances\n"+ RESETT)
        resp = client.describe_instances()

        for reservation in resp['Reservations']:
            for instances in reservation['Instances']:
                print("Id of instances: {}".format(instances['InstanceId']))
        print(RRED + "------" *10 + RESETT)
            
        
        for reserved in resp['Reservations']:
            for info in reserved['Instances']:
                
                print(Fore.LIGHTBLUE_EX + "Image ID: {}".format(info['ImageId'] + Fore.RESET))
                print("Instance ID: {}".format(info['InstanceId']))
                print("SSH Keys AWS: {}".format(info['KeyName']))
                print(info['LaunchTime'])
                print(info['Monitoring']['State'] + "\n")
                
        print(RRED + "------" *10 + Fore.RESET)
        
        for getinfo2 in resp['Reservations']:
            for info2 in getinfo2['Instances']:
                
                    print("Availability Zone: {}".format(info2['Placement']['AvailabilityZone']))
                    print("Group name: {}".format(info['Placement']['GroupName']))
                    print("Tenancy: {}".format(info['Placement']['Tenancy']  + "\n"))
        
        #print(resp)
        
        print(RRED + "------" *6 + RESETT)
        
        print(VERDE + "\n\t\tPublic options\n"  + RESETT)
        for publicinfo in resp['Reservations']:
            for pbl in publicinfo['Instances']:
                print("Your Public DNSname: " + VERDE + pbl['PublicDnsName'] + RESETT )
                print("Your Public IP: " + VERDE + pbl['PublicIpAddress']  + RESETT )
                print("Your Arch: {}".format(pbl['Architecture']))
                print("State Name: {}".format(pbl['State']['Name']))
                print("State code: " + VERDE + str(pbl['State']['Code']) + RESETT)
                print("Subnet ID: {}".format(pbl['SubnetId']))
                print("VPC ID: " + VERDE + pbl['VpcId'] + RESETT)
                
                for bdm in pbl['BlockDeviceMappings']:
                    print("Device Name: " + CYYAN + bdm['DeviceName'] + RESETT)
                    print(CYYAN + "------" *5 + RESETT)

                for element in pbl['ProductCodes']:
                    for k in element:
                        print(k + " : " + element[k])
                        print(Fore.LIGHTCYAN_EX + "------" *5 + Fore.RESET)
                        
                for dbnm in pbl['BlockDeviceMappings']:
                    for keys, values in dbnm['Ebs'].items():
                        print(keys + " : " + str(values))
                        print(Fore.LIGHTCYAN_EX + "------" *5 + Fore.RESET)
    


def main():
    tprint('hAcksWlabS')
    print(Fore.GREEN + "\tBy: Moises Tapia\t" + RESETT + VERDE + "Github: https://github.com/MoisesTapia/" + RESETT)

awsargp = parser.parse_args()

AWSIMAGE    = "ami-050184d2d97a1193f" 
AWSTYPE     = awsargp.size # t2.medium
AWSMAX      = awsargp.maxvm
AWSMIN      = awsargp.minvm
AWSKEYPAIR  = awsargp.keys


awsintances = Instance(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR)

if len(sys.argv) < 2:
    print(Fore.LIGHTGREEN_EX + 
    """
    usage mode: hackslabs.py [-h] [-z SIZE] [-mx MAXVM] [-mn MINVM] [-k KEYS]
                    [-l LAUNCH] [--stop STOP] [-s START] [-t TERMINATE]
                    [-ls LIST] [-in GETINFO]

    """
     + RESETT)
    sys.exit(1)


if awsargp.launch and awsargp.size and awsargp.maxvm and awsargp.minvm and awsargp.keys:
    main()
    print(Fore.GREEN + "\n\t\t\t\tTable of Resume" + Fore.RESET)
    print(Fore.LIGHTGREEN_EX +  "\n\t\tsave this information if you want to stop or start your instance \n" + Fore.RESET)
    awsintances.runinstance()
elif awsargp.start:
    awsintances.start_instances(awsargp.start)
elif awsargp.stop:
    awsintances.stop_instances(awsargp.stop)
elif awsargp.terminate:
    awsintances.terminate_instances(awsargp.terminate)
elif awsargp.getinfo:
    awsintances.getinfo_instances()

    
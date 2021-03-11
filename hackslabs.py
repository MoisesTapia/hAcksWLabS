#!/bin/env python
# Author: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
#

import boto3 as b3
from argparse import ArgumentParser as argp
from art import *
from colorama import Fore, init, Back, Style
#from rich.console import Console
#from rich.table import Column, Table


init()

#
# ami-050184d2d97a1193f us-west-1
# ami-0671b2fb0bfa2a568 us-east-2
# https://github.com/infoslack/awesome-web-hacking
#

client = b3.client('ec2')

#console = Console()

def parsearguments():
    
    parser = argp()
    
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
                        default="all",
                        help="list all instances in your account")

    parser.add_argument("-in" , "--getinfo", dest="getinfo",
                        type=str,
                        default="vm",
                        help="get info of your instance")
    return parser.parse_args()



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
        tprint(''' Please Wait we are running your instance''', decoration="barcode1")
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
            print("Stop instance ID: {}".format(instances['InstanceId']))
            print("Code: {}".format(instances['CurrentState']['Code']))
            print("Code: {}".format(instances['CurrentState']['Name']))
    
    def getinfo_instances(self):
        resp = client.describe_instances()
        
        print(Fore.LIGHTRED_EX + "Basic Information" + Fore.RESET)
        
        for reserved in resp['Reservations']:
            for info in reserved['Instances']:
                
                print("Image ID: {}".format(info['ImageId']))
                print("Instance ID: {}".format(info['InstanceId']))
                print(info['KeyName'])
                print(info['LaunchTime'])
                print(info['Monitoring']['State'])
        print(Fore.LIGHTRED_EX + "------------------------------------" + Fore.RESET)
        
        print(Fore.LIGHTBLUE_EX + "\n\t\tPlacement" + Fore.RESET)
        for getinfo2 in resp['Reservations']:
            for info2 in getinfo2['Placement']:
                print(info2['AvailabilityZone'])
                print(info2['HostId'])
         
        print(Fore.LIGHTGREEN_EX + "\n\t\tPlatform" + Fore.RESET)       
        for platforms in resp['Reservations']:
            print(Fore.LIGHTGREEN_EX + """
                  Information about the platform:\n
                  Platform: {}\n
                  PrivateDNS: {}\n
                  PrivateIP Address: {}
                  """.format(platforms['Platform'], platforms['PrivateDnsName'], platforms['PrivateIpAddress']) + Fore.RESET)
        
        print(Fore.LIGHTRED_EX + "------------------------------------" + Fore.RESET)
        
        print()
        for publicinfo in resp['Reservations']:
            print(publicinfo['PublicDnsName'])
            print(publicinfo['PublicIpAddress'])
            print(publicinfo['RamdiskId'])
            
    
    def list_instances(self):
        print("List of Instances and status")
        resp = client.describe_instances()

        for reservation in resp['Reservations']:
            for instances in reservation['Instances']:
                print("Id of instances: {}".format(instances['InstanceId']))


def main():
    tprint('hAcksWlabS')
    print(Fore.GREEN + "\tBy: Moises Tapia\t" + Fore.RESET + Fore.LIGHTGREEN_EX + "Github: https://github.com/MoisesTapia/" + Fore.RESET)
    print("""
        How to use: \n
          
        python3 hackslabs.py --help
          
        usage: hackslabs.py [-h] [-z SIZE] [-mx MAXVM] [-mn MINVM] [-k KEYS]
                  [-l LAUNCH] [--stop STOP] [-s START] [-t TERMINATE]
                  [-ls LIST] [-in GETINFO]

          """)

awsargp = parsearguments()

AWSIMAGE    = "ami-050184d2d97a1193f" 
AWSTYPE     = awsargp.size # t2.medium
AWSMAX      = awsargp.maxvm
AWSMIN      = awsargp.minvm
AWSKEYPAIR  = awsargp.keys


awsintances = Instance(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR)

if awsargp.launch and awsargp.size and awsargp.maxvm and awsargp.minvm and awsargp.keys:
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
    print("getinfo")
    #awsintances.getinfo_instances()
elif awsargp.list:
    print("List vms")
    #awsintances.list_instances()

if __name__ == '__main__':
    main()
    
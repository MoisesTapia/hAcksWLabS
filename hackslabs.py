#!/bin/env python
# Author: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
#

import boto3 as b3
import argparse as argp
from art import tprint
from colorama import Fore, init, Back, Style
import botocore.exceptions
import sys

VERDE = Fore.LIGHTGREEN_EX
RRED = Fore.LIGHTRED_EX
YELLOW = Fore.LIGHTYELLOW_EX
CYYAN = Fore.LIGHTCYAN_EX
RESETT = Fore.RESET




client = b3.client('ec2')

amiregiosn = {
    "us-west-1" : "ami-050184d2d97a1193f",
    "us-east-2" : "ami-0671b2fb0bfa2a568"
}

parser = argp.ArgumentParser(
    description=__doc__,
    prog="hackslabs",
    formatter_class=argp.RawDescriptionHelpFormatter,
    epilog='''
    The purpose of this script is to be able to start an instance of Kali linux in AWS 
    in which we can perform security tests in controlled environments.
    I am not responsible for the misuse that can be given to this script, 
    remember that any unauthorized computer attack is considered a cyber crime
    ''')

launch_instance = parser.add_argument_group('Launch instance')
launch_instance.add_argument("-l", "--launch",dest="launch",
                    choices=("aws","gcp","azure"),
                    help="""
                    This option requires the next attr:
                         --awstype, --maxvm, --minvm, --keypair
                    """)
launch_instance.add_argument("-z", "--awstype", dest="size", 
                    help="""choose the sice of your vm in aws, types: 
                    t2.micro, t2.small, t2.medium, t2.large, t2.xlarge.
                    Remember visit aws.com to see the cost for each vm""")
launch_instance.add_argument("-mx", "--maxvm", dest="maxvm",
                    help="Max number of the same instances",
                    type=int)
launch_instance.add_argument("-mn", "--minvm", dest="minvm",
                    help="Min number of the same instances default 1",
                    type=int)
launch_instance.add_argument( "-k", "--keypair", dest="keys",
                    help="Name of your Key Pair in AWS (ssh keys)")

instances_state = parser.add_argument_group('State of instance')
instances_state.add_argument("--stop", dest="stop",
                    help="Stop the instance or instances")
instances_state.add_argument("-s", "--start", dest="start",
                    help="Start the instance or instances")
instances_state.add_argument("-t", "--terminate",dest="terminate",
                    type=str,
                    help="""
                    Terminate the instance or instances this option will delete the instances take care""")

otheropt = parser.add_argument_group('Other Options')
otheropt.add_argument("-in" , "--getinfo", dest="getinfo",
                    type=str,
                    help="get info of your instance lista all information writting: vm")
otheropt.add_argument("-kg", "--keygen", dest="sshkeygen",
                    type=str,
                    help="This option can generate a ssh key in aws, and return information that you need save")
otheropt.add_argument("-ds", "--describe", dest="awsdescribe",
                      type=str,
                      help="Return all ssh keys stored in your AWS account")                  

versions = parser.add_argument_group('version of script')
versions.add_argument("-v", "--version",
                      version='%(prog)s 0.1.0',
                      action='version')
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
        """[summary]

        Args:
            imageid ([type]): [description]
            instancetype ([type]): [description]
            maxcount ([type]): [description]
            mincount ([type]): [description]
            keypair ([type]): [description]
        """

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
                    print("Group name: {}".format(info2['Placement']['GroupName']))
                    print("Tenancy: {}".format(info2['Placement']['Tenancy']  + "\n"))
        
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
    """
    This is just the banner of script
    """
    tprint('hAcksWlabS')
    print(Fore.GREEN + "\tBy: Moises Tapia\t" + RESETT + VERDE + "Github: https://github.com/MoisesTapia/" + RESETT)

def ssh_key_gen(keyssh):
    keypair = client.create_key_pair(KeyName=keyssh)
    
    print("Name of the SSH Key: " + VERDE + keypair.get('KeyName') + RESETT)
    print("Key Pair ID: " + RRED + keypair.get('KeyPairId') + RESETT)
    
    print("The Key Finger Print: " + CYYAN + str(keypair.get('KeyFingerprint')) + RESETT)
    
    print("Copy the next string inside of anywhere txt file: \n")
    
    print(CYYAN + keypair.get('KeyMaterial') + RESETT)
    
    print(RRED + "------" *10 + RESETT)
   
def describe_ssh_keys():
    """
    get the all information about ssh keys stored in aws
    """
    rep_describe = client.describe_key_pairs()
    # print(rep_describe) debugging response
    
    tprint('SSH Keys')
    print("-------------------------" * 3 + "\n")
    
    for key in rep_describe['KeyPairs']:
        print(YELLOW + "\t\t Information of Key \n" + RESETT)
        print("Key Fingerprint: " + RRED + str(key['KeyName']) + RESETT)
        print("Key ID: " + VERDE + str(key['KeyPairId']) + RESETT)
        print("Key Fingerprint: " + CYYAN + str(key['KeyFingerprint']) + RESETT)
        print("-------------------------" * 3 + "\n")       
    
awsargp = parser.parse_args()

AWSIMAGE    = "ami-050184d2d97a1193f" 
AWSTYPE     = awsargp.size 
AWSMAX      = awsargp.maxvm
AWSMIN      = awsargp.minvm
AWSKEYPAIR  = awsargp.keys

awsintances = Instance(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR)



#print(awsargp) debugging argparse commands

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
    try:
        print(Fore.GREEN + "\n\t\t\t\tTable of Resume" + RESETT)
        awsintances.runinstance()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.NotFound':
            print(RRED +  "\tSSH Keys not found, you need a key to connect to your instances" + RESETT)  
elif awsargp.start:
    awsintances.start_instances(awsargp.start)
elif awsargp.stop:
    awsintances.stop_instances(awsargp.stop)
elif awsargp.terminate:
    awsintances.terminate_instances(awsargp.terminate)    
elif awsargp.getinfo:
    awsintances.getinfo_instances()
elif awsargp.sshkeygen:
    print(RRED + "\n\t\tGenerating your new SSH Key " + RESETT)
    print("\tSave this key: \n")
    ssh_key_gen(awsargp.sshkeygen)
elif awsargp.awsdescribe:
    describe_ssh_keys() 
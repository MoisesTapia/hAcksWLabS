#!/bin/env python
# Maintaner: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
#

import boto3 as b3
from argparse import ArgumentParser as argp

#
# ami-050184d2d97a1193f us-west-1
# ami-0671b2fb0bfa2a568 us-east-2
# https://github.com/infoslack/awesome-web-hacking
#

client = b3.client('ec2')


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
    
    parser.add_argument("-r", "--restart",dest="restart",
                        help="Restart the instance or instances")
    
    parser.add_argument("-ls", "--list", dest="list",
                        type=str,
                        default="vm",
                        help="list all instances in your account")

    parser.add_argument("-in" , "--getinfo", dest="getinfo",
                        help="get info of your instance")
    
    parser.add_argument( "-id" ,"--instanced",dest="instanceid",
                        help="Restart the instance or instances")
    
    return parser.parse_args()



class Instance:
    """
    In this class we define the basic functions of EC2 instances like:
                - Launch
                - start
                - stop
                - terminate
                - restart
    other options 
    """

    def __init__(self, imageid, instancetype, maxcount, mincount, keypair):

        self.imageid        =   imageid
        self.instancetype   =   instancetype
        self.mincount       =   mincount
        self.maxcount       =   maxcount
        self.keypair        =   keypair
        #self.instanceid     =   instanceid
    
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
            print("Stop instance ID: {}".format(instances['InstanceId']))
            print("Code: {}".format(instances['CurrentState']['Code']))
            print("Code: {}".format(instances['CurrentState']['Name']))
    
    def getinfo(self):
        pass
    
    def list_instances(self):
        print("List of Instances and status")
        resp = client.describe_instances()

        for reservation in resp['Reservations']:
            for instances in reservation['Instances']:
                print("Id of instances: {}".format(instances['InstanceId']))




awsargp = parsearguments()

AWSIMAGE    = "ami-050184d2d97a1193f" 
AWSTYPE     = awsargp.size # t2.medium
AWSMAX      = awsargp.maxvm
AWSMIN      = awsargp.minvm
AWSKEYPAIR  = awsargp.keys


awsintances = Instance(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR)


if awsargp.launch and awsargp.size and awsargp.maxvm and awsargp.minvm and awsargp.keys:
    print("\n\t\t\t\tTable of Resume \n")
    print("\n\t\tsave this information if you want to stop your instance \n")
    awsintances.runinstance()
elif awsargp.start:
    awsintances.start_instances(awsargp.start)
elif awsargp.stop:
    awsintances.stop_instances(awsargp.stop)
elif awsargp.terminate:
    awsintances.terminate_instances(awsargp.terminate)
elif awsargp.list:
    awsintances.list_instances()
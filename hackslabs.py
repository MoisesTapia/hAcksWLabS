#!/bin/env python
import boto3 as b3
from argparse import ArgumentParser as argp

#
# ami-050184d2d97a1193f us-west-1
# ami-0671b2fb0bfa2a568 us-east-2
#
#

client = b3.client('ec2')


def parsearguments():
    
    parser = argp()
    
    parser.add_argument("--awstype", "-z", dest="size", 
                        help="""choose the sice of your vm in aws, types: 
                        t2.micro, t2.small, t2.medium, t2.large, t2.xlarge.
                        Remember visit aws.com to see the cost for each vm""")
    
    parser.add_argument("--maxvm", "-mx", dest="maxvm",
                        help="Max number of the same instances",
                        type=int)
    
    parser.add_argument("--minvm", "-mn", dest="minvm",
                        help="Min number of the same instances default 1",
                        default=1,
                        type=int)
    
    parser.add_argument("--keypair", "-k", dest="keys",
                        default='KaliLinux',
                        help="Name of your Key Pair in AWS (ssh keys)")
    
    parser.add_argument("--launch", "-l", dest="launch",
                        default="aws")
    
    parser.add_argument("--stop", dest="stop",
                        help="Stop the instance or instances")

    parser.add_argument("--start", "-s", dest="start",
                        help="Start the instance or instances")

    parser.add_argument("--terminate", "-t",dest="terminate",
                        help="""
                        Terminate the instance or instances this option will delete the instances take care""")
    
    parser.add_argument("--restart", "-r" ,dest="restart",
                        help="Restart the instance or instances")
    
    parser.add_argument("--list", "-ls" ,dest="list",
                        help="list all instances in your account")

    parser.add_argument("--getinfo", "-i" ,dest="getinfo",
                        help="get info of your instance")
    
    parser.add_argument("--instanced", "-id" ,dest="instanceid",
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

            #print("Monitoring State: ", info['Monitoring']['State'])
            #print(info['State']['Code'])
            #print(info['State']['Name'])
    
    def start_instances(self):
        print("The next instance will be available in a few minutes")
        aws_stop = client.stop_instances(InstanceIds=['i-02aa6fe76d54a8411'])
        
    def stop_instances(self):
        print("The next instance will be stop for few seconds")
        aws_stop = client.stop_instances(InstanceIds=['i-02aa6fe76d54a8411'])
        
    def terminate_instances(self):
        aws_terminate = client.terminate_instances(InstanceIds=['i-02aa6fe76d54a8411'])
    
    def restart_instance(self):
        pass
    
    def list_instances(self):
        pass
    
    def getinfo(self):
        pass



awsargp = parsearguments()


AWSIMAGE    = "ami-050184d2d97a1193f" 
AWSTYPE     = awsargp.size # t2.medium
AWSMAX      = awsargp.maxvm
AWSMIN      = awsargp.minvm
AWSKEYPAIR  = awsargp.keys

awsintances = Instance(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR)


if awsargp.launch == "aws":
    print("Your ami: {}, your insta type: {}, max instances: {}, min instances: {}, your ssh key: {}".format(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR))
    awsintances.runinstance()
elif awsargp.start == None:
    awsintances.start_instances()
elif awsargp.stop == None:
    awsintances.stop_instances()
elif awsargp.restart == None:
    awsintances.restart_instance()
elif awsargp.terminate == None:
    awsintances.terminate_instances()
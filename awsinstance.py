#!/bin/env python
import boto3 as b3

#
# ami-050184d2d97a1193f us-west-1
# ami-0671b2fb0bfa2a568 us-east-2
# ami-066c82dabe6dd7f73 testing
#

client = b3.client('ec2')


AWSIMAGE    = "ami-050184d2d97a1193f" 
AWSTYPE     = "t2.micro" # t2.medium
AWSMAX      = 1
AWSMIN      = 1
AWSKEYPAIR  = 'KaliLinux'


class Instance:

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
        pass
    def stop_instances(self):
        
        aws_stop = client.stop_instances(InstanceIds=['i-02aa6fe76d54a8411'])
        
    def terminate_instances(self):
        aws_terminate = client.terminate_instances(InstanceIds=['i-02aa6fe76d54a8411'])
    
    def list_instances(self):
        pass
    
    def getinfo(self):
        pass
        


awsintances = Instance(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR)

#awsintances.runinstance()

awsintances.getinfo()
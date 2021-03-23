#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
#

import boto3 as b3
from art import tprint
from colorama import Fore
import botocore.exceptions

VERDE = Fore.LIGHTGREEN_EX
BBLUE = Fore.LIGHTBLUE_EX
RRED = Fore.LIGHTRED_EX
YELLOW = Fore.LIGHTYELLOW_EX
CYYAN = Fore.LIGHTCYAN_EX
RESETT = Fore.RESET

client = b3.client('ec2')


#class Instance:
#    """
#    In this class we define the basic functions of EC2 instances like:
#                - Launch
#                - start
#                - stop
#                - terminate
#    other options 
#    """
#
#    def __init__(self, imageid, instancetype, maxcount, mincount, keypair):
#        """[summary]
#        Args:
#            imageid ([type]): [description]
#            instancetype ([type]): [description]
#            maxcount ([type]): [description]
#            mincount ([type]): [description]
#            keypair ([type]): [description]
#        """
#
#        self.imageid        =   imageid
#        self.instancetype   =   instancetype
#        self.mincount       =   mincount
#        self.maxcount       =   maxcount
#        self.keypair        =   keypair
#    
#    
#    def runinstance(self, imageid, instancetype, maxcount, mincount):
#        """[summary]
#        Returns:
#            [dict]: [return the response of aws]
#        """
#        resp = client.run_instances(
#            ImageId = self.imageid,
#            InstanceType = self.instancetype,
#            MinCount = self.mincount,
#            MaxCount = self.maxcount,
#            KeyName= self.keypair,
#            TagSpecifications= [
#                
#                {
#                    'ResourceType': 'instance',
#                    'Tags': [
#                        {
#                            'Key': 'Purpose',
#                            'Value': 'Pentesting Lab',
#                            'Key' : 'Name',
#                            'Value' : 'Kali Linux'
#                        },
#                    ],
#                },
#            ],
#            
#            )
#        print("\tInstance DI\t\tImage ID\t\tDate\t\t\tKey Name\tPrivate IP")
#        print("\t-----------\t\t--------\t----------------------\t\t-------\t\t----------")
#        for info in resp['Instances']:
#            print(info['InstanceId'] + "\t" + 
#                  info['ImageId'] + "\t" + 
#                  str(info['LaunchTime']) + "\t" + 
#                  info['KeyName'] + "\t" + 
#                  info['PrivateIpAddress'] )
#            
#        return resp
#    
#    def start_instances(self, instanceid):
#        """[summary]
#        Args:
#            instanceid ([string]): [start the instances in aws]
#        """
#        self.instanceid = instanceid 
#        print("The next instance will be available in a few minutes")
#        aws_start = client.start_instances(InstanceIds=[self.instanceid])
#        
#        for instances in aws_start['StartingInstances']:
#            print(" [+] Instance ID: {}".format(instances['InstanceId']))
#            print(" [+] Code ID: {}".format(instances['CurrentState']['Code']))
#            print(" [+] State ID: {}".format(instances['CurrentState']['Name']))
#        
#    def stop_instances(self,instanceid):
#        """[summary]
#        Args:
#            instanceid ([str]): [stop the instance in aws]
#        """
#        self.instanceid = instanceid
#        print(" [+] The next instance will be stop for few seconds: {}".format(self.instanceid))
#        
#        aws_stop = client.stop_instances(InstanceIds=[self.instanceid])
#        
#        for instances in aws_stop['StoppingInstances']:
#            print(" [+] Stop instance ID: {}".format(instances['InstanceId']))
#            print(" [+] Code: {}".format(instances['CurrentState']['Code']))
#            print(" [+] Code: {}".format(instances['CurrentState']['Name']))
#            
#    def terminate_instances(self,instanceid):
#        """[summary]
#        Args:
#            instanceid ([str]): [terminate the instance in aws, this function delete de instance take care]
#        """
#        self.instanceid = instanceid
#        aws_terminate = client.terminate_instances(InstanceIds=[self.instanceid])
#        
#        for instances in aws_terminate['TerminatingInstances']:
#            print(" [+] Stopping instance ID: " + RRED + instances['InstanceId'] + RESETT)
#            print(" [+] Code: {}".format(instances['CurrentState']['Code']))
#            print(" [+] Status: " + CYYAN + instances['CurrentState']['Name'] + RESETT)
#    
#    @staticmethod
#    def getinfo_instances():
#        """
#        With the boto3 library we can get the irrelevant information like:
#            ipaddress, device, name, privatedns and other attributes 
#        in this function i am recolect all information or the most important  information.
#        """
#        resp = client.describe_instances(Filters=[{
#            'Name':'instance-state-name',
#            'Values': ['running']
#        }])
#        
#        #print(resp)
#        
#        tprint('Resume')
#        
#        print(CYYAN + "\n\t\tList of Instances\n"+ RESETT)
#
#        for reservation in resp['Reservations']:
#            for instances in reservation['Instances']:
#                print("Id of instances: {}".format(instances['InstanceId']))
#        print(RRED + "------" *10 + RESETT)
#            
#        
#        for reserved in resp['Reservations']:
#            for info in reserved['Instances']:
#                
#                print(BBLUE + "Image ID: {}".format(info['ImageId'] + RESETT))
#                print(" [+] Instance ID: {}".format(info['InstanceId']))
#                print(" [+] SSH Keys AWS: {}".format(info['KeyName']))
#                print(" [+] Date: ", info['LaunchTime'])
#                print(" [+] Monitoring state: " + info['Monitoring']['State'] + "\n")
#                
#        print(RRED + "------" *10 + Fore.RESET)
#        
#        for getinfo2 in resp['Reservations']:
#            for info2 in getinfo2['Instances']:
#                    print(" [+] Availability Zone: {}".format(info2['Placement']['AvailabilityZone']))
#                    print(" [+] Group name: {}".format(info2['Placement']['GroupName']))
#                    print(" [+] Tenancy: {}".format(info2['Placement']['Tenancy']  + "\n"))
#
#        
#        for publicinfo in resp['Reservations']:
#            for pbl in publicinfo['Instances']:
#                print(RRED + "------" *6 + RESETT)
#                print(VERDE + "\n\t\tPublic options\n"  + RESETT)
#                print(" [+] Your Public DNSname: " + VERDE + pbl['PublicDnsName'] + RESETT )
#                print(" [+] Your Public IP: " + VERDE + pbl['PublicIpAddress']  + RESETT )
#                print(" [+] Your Arch: {}".format(pbl['Architecture']))
#                print(" [+] State Name: {}".format(pbl['State']['Name']))
#                print(" [+] State code: " + VERDE + str(pbl['State']['Code']) + RESETT)
#                print(" [+] Subnet ID: {}".format(pbl['SubnetId']))
#                print(" [+] VPC ID: " + VERDE + pbl['VpcId'] + RESETT)
#                
#                for bdm in pbl['BlockDeviceMappings']:
#                    print(" [+] Device Name: " + CYYAN + bdm['DeviceName'] + RESETT)
#                    print(CYYAN + "------" *5 + RESETT)
#
#                for element in pbl['ProductCodes']:
#                    for k in element:
#                        print(k + " : " + element[k])
#                        print(Fore.LIGHTCYAN_EX + "------" *5 + Fore.RESET)
#                        
#                for dbnm in pbl['BlockDeviceMappings']:
#                    for keys, values in dbnm['Ebs'].items():
#                        print(keys + " : " + str(values))
#                        print(Fore.LIGHTCYAN_EX + "------" *5 + Fore.RESET)
#


###################################### METHODS ##########################################################

def runinstance(imageid, instancetype, maxcount, mincount, keypair):
    """[summary]
    Returns:
        [dict]: [return the response of aws]
    """
    resp = client.run_instances(
        ImageId = imageid,
        InstanceType = instancetype,
        MinCount = mincount,
        MaxCount = maxcount,
        KeyName= keypair,
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

def start_instances(instanceid):
    """[summary]
    Args:
        instanceid ([string]): [start the instances in aws]
    """ 
    print("The next instance will be available in a few minutes")
    aws_start = client.start_instances(InstanceIds=[instanceid])
    
    for instances in aws_start['StartingInstances']:
        print(" [+] Instance ID: {}".format(instances['InstanceId']))
        print(" [+] Code ID: {}".format(instances['CurrentState']['Code']))
        print(" [+] State ID: {}".format(instances['CurrentState']['Name']))

def stop_instances(instanceid):
    """[summary]
    Args:
        instanceid ([str]): [stop the instance in aws]
    """
    
    print(" [+] The next instance will be stop for few seconds: {}".format(instanceid))
    
    aws_stop = client.stop_instances(InstanceIds=[instanceid])
    
    for instances in aws_stop['StoppingInstances']:
        print(" [+] Stop instance ID: {}".format(instances['InstanceId']))
        print(" [+] Code: {}".format(instances['CurrentState']['Code']))
        print(" [+] Code: {}".format(instances['CurrentState']['Name']))

def terminate_instances(instanceid):
    """[summary]
    Args:
        instanceid ([str]): [terminate the instance in aws, this function delete de instance take care]
    """
    
    aws_terminate = client.terminate_instances(InstanceIds=[instanceid])
    
    for instances in aws_terminate['TerminatingInstances']:
        print(" [+] Stopping instance ID: " + RRED + instances['InstanceId'] + RESETT)
        print(" [+] Code: {}".format(instances['CurrentState']['Code']))
        print(" [+] Status: " + CYYAN + instances['CurrentState']['Name'] + RESETT)

def getinfo_instances():
    """
    With the boto3 library we can get the irrelevant information like:
        ipaddress, device, name, privatedns and other attributes 
    in this function i am recolect all information or the most important  information.
    """
    resp = client.describe_instances(Filters=[{
        'Name':'instance-state-name',
        'Values': ['running']
    }])
    
    #print(resp)
    
    tprint('Resume')
    
    print(CYYAN + "\n\t\tList of Instances\n"+ RESETT)
    for reservation in resp['Reservations']:
        for instances in reservation['Instances']:
            print("Id of instances: {}".format(instances['InstanceId']))
    print(RRED + "------" *10 + RESETT)
        
    
    for reserved in resp['Reservations']:
        for info in reserved['Instances']:
            
            print(BBLUE + "Image ID: {}".format(info['ImageId'] + RESETT))
            print(" [+] Instance ID: {}".format(info['InstanceId']))
            print(" [+] SSH Keys AWS: {}".format(info['KeyName']))
            print(" [+] Date: ", info['LaunchTime'])
            print(" [+] Monitoring state: " + info['Monitoring']['State'] + "\n")
            
    print(RRED + "------" *10 + Fore.RESET)
    
    for getinfo2 in resp['Reservations']:
        for info2 in getinfo2['Instances']:
                print(" [+] Availability Zone: {}".format(info2['Placement']['AvailabilityZone']))
                print(" [+] Group name: {}".format(info2['Placement']['GroupName']))
                print(" [+] Tenancy: {}".format(info2['Placement']['Tenancy']  + "\n"))
    
    for publicinfo in resp['Reservations']:
        for pbl in publicinfo['Instances']:
            print(RRED + "------" *6 + RESETT)
            print(VERDE + "\n\t\tPublic options\n"  + RESETT)
            print(" [+] Your Public DNSname: " + VERDE + pbl['PublicDnsName'] + RESETT )
            print(" [+] Your Public IP: " + VERDE + pbl['PublicIpAddress']  + RESETT )
            print(" [+] Your Arch: {}".format(pbl['Architecture']))
            print(" [+] State Name: {}".format(pbl['State']['Name']))
            print(" [+] State code: " + VERDE + str(pbl['State']['Code']) + RESETT)
            print(" [+] Subnet ID: {}".format(pbl['SubnetId']))
            print(" [+] VPC ID: " + VERDE + pbl['VpcId'] + RESETT)
            
            for bdm in pbl['BlockDeviceMappings']:
                print(" [+] Device Name: " + CYYAN + bdm['DeviceName'] + RESETT)
                print(CYYAN + "------" *5 + RESETT)
            for element in pbl['ProductCodes']:
                for k in element:
                    print(k + " : " + element[k])
                    print(Fore.LIGHTCYAN_EX + "------" *5 + Fore.RESET)
                    
            for dbnm in pbl['BlockDeviceMappings']:
                for keys, values in dbnm['Ebs'].items():
                    print(keys + " : " + str(values))
                    print(Fore.LIGHTCYAN_EX + "------" *5 + Fore.RESET)
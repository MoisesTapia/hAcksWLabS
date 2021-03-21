#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
#

import boto3 as b3
from art import tprint
from colorama import Fore
import botocore.exceptions
import sys

VERDE = Fore.LIGHTGREEN_EX
BBLUE = Fore.LIGHTBLUE_EX
RRED = Fore.LIGHTRED_EX
YELLOW = Fore.LIGHTYELLOW_EX
CYYAN = Fore.LIGHTCYAN_EX
RESETT = Fore.RESET

client = b3.client('ec2')

class InstaceState:
    """[summary]This contain all functions that we need to do to get all information
    about instances.
    """

    @staticmethod
    def state_running():
        """
        Return all Vm with status running
        'Values': ['running']
        """
        resp_run = client.describe_instances(Filters=[{
            'Name':'instance-state-name',
            'Values': ['running']
        }])
        
        tprint('Runnung')
        
        for reservation in resp_run['Reservations']:
            for instances in reservation['Instances']:
                print(" [🏃] Id of instances: {}".format(instances['InstanceId']))
                print(" [🏃] Date: ", instances['LaunchTime'])
                print(" [🏃] Availability Zone: {}".format(instances['Placement']['AvailabilityZone']))
  
    @staticmethod
    def state_stopped():
        """
        Return all Vm with status stopped
        'Values': ['stopped']
        """
        resp_stopped = client.describe_instances(Filters=[{
            'Name':'instance-state-name',
            'Values': ['stopped']
        }])
        
        tprint('Stopped')

        for reservation in resp_stopped['Reservations']:
            for instances in reservation['Instances']:
                print(" [ 🛑 ] Id of instances: {}".format(instances['InstanceId']))
                print(" [ 🛑 ] Date: ", instances['LaunchTime'])
                print(" [ 🛑 ] Availability Zone: {}".format(instances['Placement']['AvailabilityZone']))

    @staticmethod
    def state_pending():
        """
        Return all Vm with status pending
        'Values': ['pending']
        """        
        resp_pending = client.describe_instances(Filters=[{
            'Name':'instance-state-name',
            'Values': ['pending']
        }])
        
        tprint('Pending')
        
        for reservation in resp_pending['Reservations']:
            for instances in reservation['Instances']:
                print(" [⌛] Id of instances: {}".format(instances['InstanceId']))
                print(" [⌛] Date: ", instances['LaunchTime'])
                print(" [⌛] Availability Zone: {}".format(instances['Placement']['AvailabilityZone']))

    @staticmethod
    def state_terminated():
        """
        Return all Vm with status terminated
        'Values': ['terminated']
        """
        resp_terminated = client.describe_instances(Filters=[{
            'Name':'instance-state-name',
            'Values': ['terminated']
        }])
        
        tprint('Terminated')
        
        for reservation in resp_terminated['Reservations']:
            for instances in reservation['Instances']:
                print(" [⚰️ ] Id of instances: {}".format(instances['InstanceId']))
                print(" [⚰️ ] Date: ", instances['LaunchTime'])
                print(" [⚰️ ] Availability Zone: {}".format(instances['Placement']['AvailabilityZone']))
                print("---" * 15 + "\n")   
        
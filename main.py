#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
#

import boto3 as b3
import argparse as argp
from art import tprint
from colorama import Fore
import botocore.exceptions
import sys

# My modules ....
from stmodules.instances import instancestate
from stmodules.instances import instances
from stmodules.shmessages import messages
from stmodules.sshkeys import sshkeys as ssk


VERDE = Fore.LIGHTGREEN_EX
BBLUE = Fore.LIGHTBLUE_EX
RRED = Fore.LIGHTRED_EX
YELLOW = Fore.LIGHTYELLOW_EX
CYYAN = Fore.LIGHTCYAN_EX
RESETT = Fore.RESET

client = b3.client('ec2')

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
launch_instance.add_argument("-l", "--launch",   dest="launch",
                    choices=("aws","gcp","azure"),
                    help="""
                    This option requires the next attr:
                         --awstype, --maxvm, --minvm, --keypair
                    """)
launch_instance.add_argument("-z", "--awstype",  dest="size", 
                    help="""choose the sice of your vm in aws, types: 
                    t2.micro, t2.small, t2.medium, t2.large, t2.xlarge.
                    Remember visit aws.com to see the cost for each vm""")
launch_instance.add_argument("-mx", "--maxvm",   dest="maxvm",
                    help="Max number of the same instances",
                    type=int)
launch_instance.add_argument("-mn", "--minvm",   dest="minvm",
                    help="Min number of the same instances default 1",
                    type=int)
launch_instance.add_argument( "-k", "--keypair", dest="keys",
                    help="Name of your Key Pair in AWS (ssh keys)")

instances_state = parser.add_argument_group('State of instance')
instances_state.add_argument("--stop",            dest="stop",
                    help="Stop the instance or instances")
instances_state.add_argument("-s", "--start",     dest="start",
                    help="Start the instance or instances")
instances_state.add_argument("-t", "--terminate", dest="terminate",
                    type=str,
                    help="""
                    Terminate the instance or instances this option will delete the instances take care""")

instance_status = parser.add_argument_group('Filter Instances for')
instance_status.add_argument("-sr", "--state-runnig", dest="running",
                             help="Return a list of the instances with status running", type=str)
instance_status.add_argument("-st", "--state-terminated", dest="terminated",
                             help="Return a list of the instances with status terminated", type=str)
instance_status.add_argument("-sp", "--state-pending", dest="pending",
                             help="Return a list of the instances with status pending", type=str)
instance_status.add_argument("-se", "--state-stopped", dest="stopped",
                             help="Return a list of the instances with status stopped", type=str)

versions = parser.add_argument_group('version of script')
versions.add_argument("-v", "--version",
                      version='%(prog)s 0.1.0',
                      action='version')
versions.add_argument("-at","--author", dest="authors",
                      type=str,
                      help="Information about the author")

otheropt = parser.add_argument_group('Other Options')
otheropt.add_argument("-in" , "--getinfo", dest="getinfo",
                    type=str,
                    help="get info of your instance lista all information writting: vm")
otheropt.add_argument("-kg", "--keygen", dest="sshkeygen",
                    type=str,
                    help="This option can generate a ssh key in aws, and return information that you need save")
otheropt.add_argument("-ds", "--describe", dest="awsdescribe",
                      type=str,help="Return all ssh keys stored in your AWS account")                  
otheropt.add_argument("-kn", "--key-name", dest="kgname",
                      type=str,
                      help="Name of the file where the will be save it, by default is saved without extension")
otheropt.add_argument("-it", "--intances-types",dest="instances",
                      type=str,
                      help="Show the table of instances")


awsargp = parser.parse_args()

AWSIMAGE    = "ami-050184d2d97a1193f" 
AWSTYPE     = awsargp.size 
AWSMAX      = awsargp.maxvm
AWSMIN      = awsargp.minvm
AWSKEYPAIR  = awsargp.keys

#print(awsargp) debugging argparse commands

if len(sys.argv) < 2:
    messages.print_help()
    sys.exit(1)

if awsargp.launch and awsargp.size and awsargp.maxvm and awsargp.minvm and awsargp.keys:
    messages.main()
    try:
        print(Fore.GREEN + "\n\t\t\t\tTable of Resume" + RESETT)
        instances.runinstance(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.NotFound':
            print(RRED +  "\tSSH Keys not found, you need a key to connect to your instances" + RESETT)  
elif awsargp.launch and awsargp.size and awsargp.maxvm and awsargp.minvm and not awsargp.keys:
    print(RRED + "\n\t\tSet your AWS SSH Keys ... " + RESETT)
    print(RRED + """
          \n\t\tIf you do not have ssh keys you can generate a new ssh keys...
           python3 hackslabs.py -kg <name_key> -kn name.txt/.pem
          """ + RESETT)
elif awsargp.launch and not awsargp.size and awsargp.maxvm and awsargp.minvm and awsargp.keys:
    print(RRED + "\n\t\tSet the type of instance ... " + RESETT + "\n")
    print("\t\tSee more in: " + VERDE + "https://aws.amazon.com/ec2/instance-types/" + RESETT)   
elif awsargp.start:
    instances.start_instances(awsargp.start)
elif awsargp.stop:
    instances.stop_instances(awsargp.stop)
elif awsargp.terminate:
    instances.terminate_instances(awsargp.terminate)    
elif awsargp.getinfo == "vm":
    instances.getinfo_instances()
elif awsargp.sshkeygen and awsargp.kgname:
    print(RRED + "\n\t\tGenerating your new SSH Key " + RESETT)
    ssk.ssh_key_gen(awsargp.sshkeygen, awsargp.kgname)
elif awsargp.sshkeygen and not awsargp.kgname:
    print(RRED + "\n\t\tPlease Set the name of your File ... " + RESETT)
    print(CYYAN + "\n\t\tusage mode: python3 hackslabs.py -kg <name_key> -kn name.txt/.pem" + RESETT + "\n")
elif awsargp.awsdescribe == "list":
    ssk.describe_ssh_keys()
elif awsargp.running == "vm":
    instancestate.state_running
elif awsargp.stopped == "vm":
    instancestate.state_stopped()
elif awsargp.terminated == "vm":
    instancestate.state_terminated()
elif awsargp.pending == "vm":
    instancestate.state_pending()
elif awsargp.instances == "show":
    messages.types_instances()
elif awsargp.authors == "list":
    messages.script_authors()
else:
    print("\n" + "▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀" * 4)
    tprint('Error 404', font="knob")
    print("▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀" * 4 + "\n")
    messages.print_help()

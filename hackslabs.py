#!usr/bin/python
# Author: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
# Twitter: 

import boto3 as b3
import argparse as argp
from argparse_color_formatter import ColorHelpFormatter
from rich.console import Console
from rich.table import Column, Table
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
console = Console()

#amiregiosn = {
#    "us-west-1" : "ami-050184d2d97a1193f",
#    "us-east-2" : "ami-0671b2fb0bfa2a568"
#}


parser = argp.ArgumentParser(
    description=__doc__,
    prog="hackslabs",
    formatter_class=ColorHelpFormatter, #argp.RawDescriptionHelpFormatter
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




class InstaceState():
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
        """[summary]
        Returns:
            [dict]: [return the response of aws]
        """
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
        """[summary]
        Args:
            instanceid ([string]): [start the instances in aws]
        """
        self.instanceid = instanceid 
        print("The next instance will be available in a few minutes")
        aws_start = client.start_instances(InstanceIds=[self.instanceid])
        
        for instances in aws_start['StartingInstances']:
            print(" [+] Instance ID: {}".format(instances['InstanceId']))
            print(" [+] Code ID: {}".format(instances['CurrentState']['Code']))
            print(" [+] State ID: {}".format(instances['CurrentState']['Name']))
        
    def stop_instances(self,instanceid):
        """[summary]
        Args:
            instanceid ([str]): [stop the instance in aws]
        """
        self.instanceid = instanceid
        print(" [+] The next instance will be stop for few seconds: {}".format(self.instanceid))
        
        aws_stop = client.stop_instances(InstanceIds=[self.instanceid])
        
        for instances in aws_stop['StoppingInstances']:
            print(" [+] Stop instance ID: {}".format(instances['InstanceId']))
            print(" [+] Code: {}".format(instances['CurrentState']['Code']))
            print(" [+] Code: {}".format(instances['CurrentState']['Name']))
            
    def terminate_instances(self,instanceid):
        """[summary]
        Args:
            instanceid ([str]): [terminate the instance in aws, this function delete de instance take care]
        """
        self.instanceid = instanceid
        aws_terminate = client.terminate_instances(InstanceIds=[self.instanceid])
        
        for instances in aws_terminate['TerminatingInstances']:
            print(" [+] Stopping instance ID: " + RRED + instances['InstanceId'] + RESETT)
            print(" [+] Code: {}".format(instances['CurrentState']['Code']))
            print(" [+] Status: " + CYYAN + instances['CurrentState']['Name'] + RESETT)
    
    @staticmethod
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

def main():
    """
    This is just the banner of script.
    Welcome banner
    """
    tprint('hAcksWlabS')
    print(Fore.GREEN + "\tBy: Moises Tapia\t" + RESETT + VERDE + "Github: https://github.com/MoisesTapia/" + RESETT)

def print_help():
    """Print the first Main is the srcrip do not recive some argument"""
    print(Fore.LIGHTGREEN_EX + 
    """
    basic commands: hackslabs.py [-h] [-z SIZE] [-mx MAXVM] [-mn MINVM] [-k KEYS]
                    [-l LAUNCH] [--stop STOP] [-s START] [-t TERMINATE]
                    [-ls LIST] [-in GETINFO]
    """
     + RESETT)
    
    print(CYYAN + 
        """
        Usage Mode:
            Launch Instances:
            python3 hackslabs.py -l aws -z t2.micro -mx 1 -mn 1 -k KaliLinux
            
            Get help:
            python3 hackslabs.py --help/-h
            
            termibate instances 
            python3 hackslabs.py --terminate/t <id_instances>
            
        """ + RESETT)
    
def ssh_key_gen(keyssh, ssh_keyname):
    """[summary]
    Args:
        keyssh ([str]): [create a new ssh keys in aws]
    """
    try:
        file_name = ssh_keyname
        keypair = client.create_key_pair(KeyName=keyssh)
        encode_key = keypair.get('KeyMaterial')
        
        print("[✔]" + "Name of the SSH Key: " + VERDE + keypair.get('KeyName') + RESETT)
        print("[✔]" + "Key Pair ID: " + RRED + keypair.get('KeyPairId') + RESETT)
        print("[✔]" + "The Key Finger Print: " + CYYAN + str(keypair.get('KeyFingerprint')) + RESETT)

        print("\n[+] Your key was generated and saved in the file named : \n")

        f= open(file_name,"w+")
        f.writelines(encode_key)
        print(" [✔] file name: " + VERDE +  f.name + RESETT + "\n")
        f.close()
        print(RRED + "------" *10 + RESETT)
         
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidKeyPair.Duplicate':
            print(RRED + "\n\t\t[X] " + CYYAN + "Error occurred the keys already exist" + RESETT + "\n")
            print(VERDE + "\t\tList the existent Keys with: " + BBLUE + " -ds" + RESETT + "\n")

def describe_ssh_keys():
    """Get the all information about ssh keys stored in aws"""
    rep_describe = client.describe_key_pairs()
    # print(rep_describe) debugging response
    
    tprint('SSH Keys')
    print("-------------------------" * 3 + "\n")
    
    for key in rep_describe['KeyPairs']:
        print(YELLOW + "\t\t Information of Key \n" + RESETT)
        print(" [✔] Key Fingerprint: " + RRED + str(key['KeyName']) + RESETT)
        print(" [✔] Key ID: " + VERDE + str(key['KeyPairId']) + RESETT)
        print(" [✔] Key Fingerprint: " + CYYAN + str(key['KeyFingerprint']) + RESETT)
        print("-------------------------" * 3 + "\n")       
    
def types_instances():
    """Print:
    The table with all instances types in aws in wich you can deploy your Kali Linux VM
    """
    authors = Table(show_header=True, header_style="bold green")
    authors.add_column("Type", style="dim", justify="center")
    authors.add_column("vCPU*", style="dim", justify="center")
    authors.add_column("CPU Credits / hour", style="dim", justify="center")
    authors.add_column("Mem GiB", style="dim", justify="center")
    authors.add_column("Storage", style="dim", justify="center")
    authors.add_column("Network Performance", style="dim", justify="center")
    authors.add_row(
        "t2.nano",
        "1",
        "3",
        "0.5",
        "EBS-Only",
        "Low"
    )
    authors.add_row(
        "t2.micro",
        "1",
        "6",
        "1",
        "EBS-Only",
        "Low to Moderate"
    )
    authors.add_row(
        "t2.small",
        "1",
        "12",
        "2",
        "EBS-Only",
        "Low to Moderate"
    )
    authors.add_row(
        "t2.medium",
        "2",
        "24",
        "4",
        "EBS-Only",
        "Low to Moderate"
    )
    authors.add_row(
        "t2.large",
        "2",
        "36",
        "8",
        "EBS-Only",
        "Low to Moderate"
    )
    authors.add_row(
        "t2.xlarge",
        "4",
        "54",
        "16",
        "EBS-Only",
        "Moderate"
    )
    authors.add_row(
        "t2.2xlarge",
        "8",
        "81",
        "32",
        "EBS-Only",
        "Moderate"
    )
    console.print(authors)
    
def script_authors():
    """Print the all contributors"""
    authors = Table(show_header=True, header_style="bold green")
    authors.add_column("Username", style="dim", justify="center")
    authors.add_column("Name", style="dim", justify="center")
    authors.add_column("Twitter", style="dim", justify="center")
    authors.add_column("Url", style="dim", justify="center")
    authors.add_row(
        "moisestapia",
        "Moises Tapia",
        "@equinockx",
        "https://github.com/MoisesTapia"
    )
    console.print(authors)

awsargp = parser.parse_args()

AWSIMAGE    = "ami-050184d2d97a1193f" 
AWSTYPE     = awsargp.size 
AWSMAX      = awsargp.maxvm
AWSMIN      = awsargp.minvm
AWSKEYPAIR  = awsargp.keys


awsintances = Instance(AWSIMAGE, AWSTYPE, AWSMAX, AWSMIN, AWSKEYPAIR)

getstatus = InstaceState()

#print(awsargp) debugging argparse commands

if len(sys.argv) < 2:
    print_help()
    sys.exit(1)

if awsargp.launch and awsargp.size and awsargp.maxvm and awsargp.minvm and awsargp.keys:
    main()
    try:
        print(Fore.GREEN + "\n\t\t\t\tTable of Resume" + RESETT)
        awsintances.runinstance()
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
    awsintances.start_instances(awsargp.start)
elif awsargp.stop:
    awsintances.stop_instances(awsargp.stop)
elif awsargp.terminate:
    awsintances.terminate_instances(awsargp.terminate)    
elif awsargp.getinfo == "vm":
    awsintances.getinfo_instances()
elif awsargp.sshkeygen and awsargp.kgname:
    print(RRED + "\n\t\tGenerating your new SSH Key " + RESETT)
    ssh_key_gen(awsargp.sshkeygen, awsargp.kgname)
elif awsargp.sshkeygen and not awsargp.kgname:
    print(RRED + "\n\t\tPlease Set the name of your File ... " + RESETT)
    print(CYYAN + "\n\t\tusage mode: python3 hackslabs.py -kg <name_key> -kn name.txt/.pem" + RESETT + "\n")
elif awsargp.awsdescribe == "list":
    describe_ssh_keys()
elif awsargp.running == "vm":
    getstatus.state_running()
elif awsargp.stopped == "vm":
    getstatus.state_stopped()
elif awsargp.terminated == "vm":
    getstatus.state_terminated()
elif awsargp.pending == "vm":
    getstatus.state_pending()
elif awsargp.instances == "show":
    types_instances()
elif awsargp.authors == "list":
    script_authors()
else:
    print("\n" + "▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀" * 4)
    tprint('Error 404', font="knob")
    print("▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀" * 4 + "\n")
    print_help()

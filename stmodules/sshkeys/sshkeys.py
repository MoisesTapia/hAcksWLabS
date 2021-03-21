#!usr/bin/python
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



def ssh_key_gen(keyssh, ssh_keyname):
    """[summary]
    Args:
        keyssh ([str]): [create a new ssh keys in aws]
    """
    try:
        file_name = ssh_keyname
        keypair = client.create_key_pair(KeyName=keyssh)
        encode_key = keypair.get('KeyMaterial')
        
        print("[🔐]" + "Name of the SSH Key: " + VERDE + keypair.get('KeyName') + RESETT)
        print("[🔐]" + "Key Pair ID: " + RRED + keypair.get('KeyPairId') + RESETT)
        print("[🔐]" + "The Key Finger Print: " + CYYAN + str(keypair.get('KeyFingerprint')) + RESETT)
        print("\n[+] Your key was generated and saved in the file named : \n")
        
        f= open(file_name,"w+")
        f.writelines(encode_key)
        print(" [🔐] file name: " + VERDE +  f.name + RESETT + "\n")
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
        print(" [🔐] Key Fingerprint: " + RRED + str(key['KeyName']) + RESETT)
        print(" [🔐] Key ID: " + VERDE + str(key['KeyPairId']) + RESETT)
        print(" [🔐] Key Fingerprint: " + CYYAN + str(key['KeyFingerprint']) + RESETT)
        print("-------------------------" * 3 + "\n")  
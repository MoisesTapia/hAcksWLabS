#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moises Tapia(equinockx)
# Github: https://github.com/MoisesTapia
#

from art import tprint
from colorama import Fore
import botocore.exceptions
from rich.console import Console
from rich.table import Column, Table
import sys

console = Console()

VERDE = Fore.LIGHTGREEN_EX
BBLUE = Fore.LIGHTBLUE_EX
RRED = Fore.LIGHTRED_EX
YELLOW = Fore.LIGHTYELLOW_EX
CYYAN = Fore.LIGHTCYAN_EX
RESETT = Fore.RESET

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

def types_instances():
    """Print:
    The table with all instances types in aws in wich you can deploy your Kali Linux VM
    """
    instances_types = Table(show_header=True, header_style="bold green")
    instances_types.add_column("Type", style="dim", justify="center")
    instances_types.add_column("vCPU*", style="dim", justify="center")
    instances_types.add_column("CPU Credits / hour", style="dim", justify="center")
    instances_types.add_column("Mem GiB", style="dim", justify="center")
    instances_types.add_column("Storage", style="dim", justify="center")
    instances_types.add_column("Network Performance", style="dim", justify="center")
    
    instances_types.add_row(
        "t2.nano",
        "1",
        "3",
        "0.5",
        "EBS-Only",
        "Low"
    )
    instances_types.add_row(
        "t2.micro",
        "1",
        "6",
        "1",
        "EBS-Only",
        "Low to Moderate"
    )
    instances_types.add_row(
        "t2.small",
        "1",
        "12",
        "2",
        "EBS-Only",
        "Low to Moderate"
    )
    instances_types.add_row(
        "t2.medium",
        "2",
        "24",
        "4",
        "EBS-Only",
        "Low to Moderate"
    )
    instances_types.add_row(
        "t2.large",
        "2",
        "36",
        "8",
        "EBS-Only",
        "Low to Moderate"
    )
    instances_types.add_row(
        "t2.xlarge",
        "4",
        "54",
        "16",
        "EBS-Only",
        "Moderate"
    )
    instances_types.add_row(
        "t2.2xlarge",
        "8",
        "81",
        "32",
        "EBS-Only",
        "Moderate"
    )
    console.print(instances_types)

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
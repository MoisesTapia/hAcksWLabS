import boto3 as b3

client = b3.client('ec2')
vpc = b3.resource('ec2')

CIDRBlOCK = '172.16.0.0/16'



class AwsVPC:
    
    def __init__(self, cidrblock):
        self.cidrblock = cidrblock
    
    
    
    def deploy_vpc(self):
        vpcblock = vpc.create_vpc(CidrBlock=self.cidrblock)
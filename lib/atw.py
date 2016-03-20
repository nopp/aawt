#
# ATW - AWS Tool Web
#
import ConfigParser
import boto3
import sys

config = ConfigParser.RawConfigParser()
config.read('/etc/atw/config.cfg')

class Atw:

    access_key = config.get('conf','accessKey')
    secret_key = config.get('conf','secretKey')    
    
    # This is a little hammer, I'll fix this soon :D    
    def menu(self):
        menu = config.get('conf','regions')
        return menu.split(",")    
    
    # This is a little hammer, I'll fix this soon :D
    def error(self,message):
        error = []
        eMsg = [message]
        error.append(eMsg)
        return error

    # Connect to resource
    def connect_resource(self,region,resource):
        try:
            session = boto3.session.Session(aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=region)
            conn = session.resource(resource)
            return conn
        except:			
            return self.error("Error - can't connect to "+resource+" (LIB)")

    # Connect to client
    def connect_client(self,region,client):
        try:
            conn = boto3.client(client,aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=region)
            return conn
        except:
            return self.error("Error - can't connect to "+client+" (LIB)")

    # Return EC2 Tags
    def returnTags(self,tags):
        ec2Tags = []
        tag = {}
        for numIndice in range(0,len(tags)):
            tag = {tags[numIndice].values()[1]:tags[numIndice].values()[0]}
            ec2Tags.append(tag)
        return ec2Tags

    # Return value by Tag
    def returnTagEC2(self,ec2Tags,tag):
        for i in range(len(ec2Tags)):
            if ec2Tags[i].keys()[0] == tag:
                return ec2Tags[i].values()[0]

    # EC2 List all
    def ec2_listAll(self,region):
        ec2_res = self.connect_resource(region,"ec2")
        ec2List = []
        for ec2 in ec2_res.instances.all():
            tagList = self.returnTags(ec2.tags)
            ec2Vm = [self.returnTagEC2(tagList,"Name"),ec2.instance_id,ec2.private_ip_address,ec2.instance_type,ec2.state['Name'],ec2.placement['AvailabilityZone'],tagList,ec2.public_ip_address,ec2.platform]
            ec2List.append(ec2Vm)
        return ec2List

    # EC2 total
    def ec2_total(self,region):
        ec2_res = self.connect_resource(region,"ec2")
        total = 0
        for ec2 in ec2_res.instances.all():
            total=total+1
        return total
    
    # EC2 total EBS
    def ec2_totalEbs(self,region,opt):
        ec2 = self.connect_client(region,"ec2")
        total = 0
        if opt == "size":
            # Size
            for volume in ec2.describe_volumes()['Volumes']:
                total = total+volume['Size']         
        else:
            # Total
            for volume in ec2.describe_volumes()['Volumes']:
                total = total+1
        return total

    # RDS List all
    def rds_listAll(self,region):
        rdsClient = self.connect_client(region,"rds")
        try:
            rdsList = []
            for rds in rdsClient.describe_db_instances()['DBInstances']:
                rdsIntance = [rds['DBName'],rds['Engine'],rds['MasterUsername'],rds['Endpoint']['Address'],rds['Endpoint']['Port'],rds['DBInstanceStatus']]
                rdsList.append(rdsIntance)
            return rdsList
        except:
            return self.error("Error - Can't list all RDS (LIB)")
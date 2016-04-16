
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
            return self.error("ErrorLib - can't connect to "+resource+".")

    # Connect to client
    def connect_client(self,region,client):
        try:
            if region == "":
                conn = boto3.client(client,aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key)
            else:
                conn = boto3.client(client,aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=region)
            return conn
        except:
            return self.error("ErrorLib - can't connect to "+client+".")

    # EC2 return info
    def ec2_info(self,region,id,ec2_res):
        if ec2_res == "":
            ec2_res = self.connect_resource(region,"ec2")
        try:
            instance = ec2_res.Instance(id)
            ec2Info = {}
            ec2Info['name'] = self.returnTagEC2(self.returnTags(instance.tags),"Name")
            ec2Info['instance_id'] = id
            ec2Info['image_id'] = instance.image_id
            ec2Info['instance_type'] = instance.instance_type
            ec2Info['launch_time'] = instance.launch_time.strftime('%d/%m/%Y %H:%M:%S')
            ec2Info['network_interfaces'] = instance.network_interfaces
            ec2Info['platform'] = instance.platform
            ec2Info['private_ip_address'] = instance.private_ip_address
            ec2Info['public_ip_address'] = instance.public_ip_address
            ec2Info['security_groups'] = instance.security_groups
            ec2Info['state'] = instance.state['Name']
            ec2Info['subnet_id'] = instance.subnet_id
            ec2Info['vpc'] = instance.vpc
            ec2Info['tagList'] = self.returnTags(instance.tags)
            ec2Info['placement'] = instance.placement['AvailabilityZone']
            return ec2Info
        except:
            return self.error("ErrorLib - Can't return ec2 info.")

    # Return EC2 Tags
    def returnTags(self,tags):
        try:
            ec2Tags = []
            tag = {}
            for numIndice in range(0,len(tags)):
                tag = {tags[numIndice].values()[1]:tags[numIndice].values()[0]}
                ec2Tags.append(tag)
            return ec2Tags
        except:
            return self.error("ErrorLib - Can't return all tags.")

    # Return value by Tag
    def returnTagEC2(self,ec2Tags,tag):
        try:
            for i in range(len(ec2Tags)):
                if ec2Tags[i].keys()[0] == tag:
                    return ec2Tags[i].values()[0]
        except:
            return self.error("ErrorLib - Can't return tag "+tag+".")

    # EC2 List all
    def ec2_listAll(self,region):
        ec2_res = self.connect_resource(region,"ec2")
        try:
            ec2List = []
            for ec2 in ec2_res.instances.all():
                ec2Info = {}
                ec2Info['name'] = self.returnTagEC2(self.returnTags(ec2.tags),"Name")
                ec2Info['instance_id'] = ec2.instance_id
                ec2Info['instance_type'] = ec2.instance_type
                ec2Info['platform'] = ec2.platform
                ec2Info['private_ip_address'] = ec2.private_ip_address
                ec2Info['public_ip_address'] = ec2.public_ip_address
                ec2Info['state'] = ec2.state['Name']
                ec2Info['tagList'] = self.returnTags(ec2.tags)
                ec2Info['placement'] = ec2.placement['AvailabilityZone']
                ec2List.append(ec2Info)
            return ec2List
        except:
            return self.error("ErrorLib - Can't list all ec2.")

    # EC2 total
    def ec2_total(self,region):
        ec2_res = self.connect_resource(region,"ec2")
        try:
            total = 0
            for ec2 in ec2_res.instances.all():
                total=total+1
            return total
        except:
            return self.error("ErrorLib - Can't return total of ec2.")
    
    # EC2 total EBS
    def ec2_totalEbs(self,region,opt):
        ec2 = self.connect_client(region,"ec2")
        try:
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
        except:
            return self.error("ErrorLib - Can't list all ebs.")

    # EC2 reserved list all active
    def ec2r_listAll(self,region):
        ec2r = self.connect_client(region,"ec2")
        try:
            reservedList = []
            totalReserved = 0
            for ec2Reserved in ec2r.describe_reserved_instances()['ReservedInstances']:
                if ec2Reserved['State'] == "active":
                    reservedInfo = {}
                    reservedInfo['InstanceCount'] = ec2Reserved['InstanceCount']
                    reservedInfo['OfferingType'] = ec2Reserved['OfferingType']
                    reservedInfo['InstanceType'] = ec2Reserved['InstanceType']
                    reservedInfo['AvailabilityZone'] = ec2Reserved['AvailabilityZone']
                    reservedInfo['ProductDescription'] = ec2Reserved['ProductDescription']
                    reservedInfo['State'] = ec2Reserved['State']
                    reservedInfo['Start'] = ec2Reserved['Start'].strftime("%d/%m/%Y")
                    reservedInfo['End'] = ec2Reserved['End'].strftime("%d/%m/%Y")
                    reservedInfo['Term'] = ec2Reserved['End'].year-ec2Reserved['Start'].year
                    reservedInfo['ReservedInstancesId'] = ec2Reserved['ReservedInstancesId'].split("-")[0]
                    totalReserved = totalReserved+ec2Reserved['InstanceCount']
                    reservedList.append(reservedInfo)
            return reservedList,totalReserved
        except:
            return self.error("ErrorLib - Can't list all EC2 reserved.")

    # RDS List all
    def rds_listAll(self,region):
        rdsClient = self.connect_client(region,"rds")
        try:
            rdsList = []
            for rds in rdsClient.describe_db_instances()['DBInstances']:
                rdsIntance = {}
                rdsIntance['Name'] = rds['DBName']
                rdsIntance['Engine'] = rds['Engine']
                rdsIntance['MasterUsername'] = rds['MasterUsername']
                rdsIntance['Endpoint'] = rds['Endpoint']['Address']
                rdsIntance['Port'] = rds['Endpoint']['Port']
                rdsIntance['DBInstanceStatus'] = rds['DBInstanceStatus']
                rdsList.append(rdsIntance)
            return rdsList
        except:
            return self.error("ErrorLib - Can't list all RDS.")
    
    # ELB List all
    def elb_listAll(self,region):
        elbClient = self.connect_client(region,"elb")
        try:
            elbList = []
            for elb in elbClient.describe_load_balancers()['LoadBalancerDescriptions']:
                elbInfo = {}
                elbInfo['Scheme'] = elb['Scheme']
                elbInfo['LoadBalancerName'] = elb['LoadBalancerName']
                elbInfo['DNSName'] = elb['DNSName']
                elbInfo['Instances'] = elb['Instances']
                elbList.append(elbInfo)
            return elbList
        except:
            return self.error("ErrorLib - Can't list all elb.")

    # IAM List all
    def iam_listAll(self):
        iamClient = self.connect_client("","iam")
        try:
            iamList = []
            for user in iamClient.list_users()['Users']:
                keys = []
                for awskey in iamClient.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']:
                    keys.append(awskey['AccessKeyId'])
                iamInfo = [user['UserName'],keys]
                iamList.append(iamInfo)
            return iamList
        except:
            return self.error("ErrorLib - Can't list all users.")

    # EBS List all
    def ebs_listAll(self,region):
        ebsClient = self.connect_client(region,"ec2")
        try:
            ebsType = {
                "gp2": 'General Purpose SSD',
                "io1": 'Provisioned IOPS SSD',
                "standard": 'Magnetic',
            }
            ebsList = []
            total = 0
            for vol in ebsClient.describe_volumes()['Volumes']:
                ebsInfo = {}
                total = total+vol['Size']
                ebsInfo['VolumeId'] = vol['VolumeId']
                ebsInfo['VolumeType'] = ebsType[vol['VolumeType']]
                ebsInfo['Size'] = vol['Size']
                ebsInfo['AvailabilityZone'] = vol['AvailabilityZone']
                ebsInfo['State'] = vol['State']
                ebsInfo['InstanceId'] = vol['Attachments'][0]['InstanceId']
                ebsList.append(ebsInfo)
            return ebsList,total
        except:
            return self.error("ErrorLib - Can't list all ebs.")
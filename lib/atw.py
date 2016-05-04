#
# ATW - AWS Tool Web
#
import ConfigParser
import datetime
import boto3
import pygal
import sys
from pygal.style import Style

config = ConfigParser.RawConfigParser()
config.read('/etc/atw/config.cfg')

class Atw:

    access_key = config.get('conf','accessKey')
    secret_key = config.get('conf','secretKey')
     
    def menu(self):
        try:
            menu = config.get('conf','regions')
            return menu.split(",")
        except:
            return "ErrorLib - can't get menu."

    # Connect to resource
    def connect_resource(self,region,resource):
        try:
            session = boto3.session.Session(aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=region)
            conn = session.resource(resource)
            return conn
        except:			
            return "ErrorLib - can't connect to "+resource+"."

    # Connect to client
    def connect_client(self,region,client):
        try:
            if region == "":
                conn = boto3.client(client,aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key)
            else:
                conn = boto3.client(client,aws_access_key_id=self.access_key,aws_secret_access_key=self.secret_key,region_name=region)
            return conn
        except:
            return "ErrorLib - can't connect to "+client+"."

    # EC2 return info
    def ec2_info(self,region,id,ec2_res):
        try:
            if ec2_res == "":
                ec2_res = self.connect_resource(region,"ec2")
            instance = ec2_res.Instance(id)
            return instance
        except:
            return "ErrorLib - Can't return EC2 info."

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
            return "ErrorLib - Can't return all TAGS."

    # Return value by Tag
    def returnTagEC2(self,ec2Tags,tag):
        try:
            for i in range(len(ec2Tags)):
                if ec2Tags[i].keys()[0] == tag:
                    return ec2Tags[i].values()[0]
        except:
            return "ErrorLib - Can't return tag "+tag+"."

    # EC2 List all
    def ec2_listAll(self,region):
        try:
            ec2_res = self.connect_resource(region,"ec2")
            ec2List = []
            for ec2 in ec2_res.instances.all():
                ec2List.append(ec2)
            return ec2List
        except:
            return "ErrorLib - Can't list all EC2."

    # EC2 total
    def ec2_total(self,region):
        try:
            ec2_res = self.connect_resource(region,"ec2")
            total = 0
            for ec2 in ec2_res.instances.all():
                total=total+1
            return total
        except:
            return "ErrorLib - Can't return total of EC2."
    
    # EC2 total EBS
    def ec2_totalEbs(self,region,opt):
        try:
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
        except:
            return "ErrorLib - Can't list all EBS."

    # EC2 reserved - list all active
    def ec2r_listAll(self,region):
        try:
            ec2r = self.connect_client(region,"ec2")
            reservedList = []
            totalReserved = 0
            for ec2Reserved in ec2r.describe_reserved_instances()['ReservedInstances']:
                if ec2Reserved['State'] == "active":
                    totalReserved = totalReserved+ec2Reserved['InstanceCount']
                    reservedList.append(ec2Reserved)
            return reservedList,totalReserved
        except:
            return "ErrorLib - Can't list all EC2 reserved."

    # RDS List all
    def rds_listAll(self,region):
        try:
            rdsClient = self.connect_client(region,"rds")
            rdsList = []
            for rds in rdsClient.describe_db_instances()['DBInstances']:
                rdsList.append(rds)
            return rdsList
        except:
           return "ErrorLib - Can't list all RDS."
    
    # ELB List all
    def elb_listAll(self,region):
        try:
            elbClient = self.connect_client(region,"elb")
            elbList = []
            for elb in elbClient.describe_load_balancers()['LoadBalancerDescriptions']:
                elbList.append(elb)
            return elbList
        except:
            return "ErrorLib - Can't list all ELB."

    # IAM List all
    def iam_listAll(self):
        try:
            iamClient = self.connect_client("","iam")
            iamList = []
            for user in iamClient.list_users()['Users']:
                keys = []
                for awskey in iamClient.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']:
                    keys.append(awskey['AccessKeyId'])
                iamInfo = [user['UserName'],keys]
                iamList.append(iamInfo)
            return iamList
        except:
            return "ErrorLib - Can't list all users."

    # EBS List all
    def ebs_listAll(self,region):
        try:
            ebsClient = self.connect_client(region,"ec2")
            ebsList = []
            total = 0
            for ebs in ebsClient.describe_volumes()['Volumes']:
                total = total+ebs['Size']
                ebsList.append(ebs)
            return ebsList,total
        except:
            return "ErrorLib - Can't list all EBS."

    # Billing
    def charge_service(self,service,option=None):
        try:
            chargeClient = self.connect_client('us-east-1','cloudwatch')
            if option == "total":
                response = chargeClient.get_metric_statistics(
                    Namespace='AWS/Billing',
                    MetricName='EstimatedCharges',
                    StartTime=datetime.datetime.now() - datetime.timedelta(minutes=300),
                    EndTime=datetime.datetime.now(),
                    Period=21600,
                    Statistics=['Maximum'],
                    Dimensions=[{'Name':'Currency','Value':'USD'}]
                )
            else:
                response = chargeClient.get_metric_statistics(
                    Namespace='AWS/Billing',
                    MetricName='EstimatedCharges',
                    StartTime=datetime.datetime.now() - datetime.timedelta(minutes=300),
                    EndTime=datetime.datetime.now(),
                    Period=21600,
                    Statistics=['Maximum'],
                    # Services AmazonEC2, AmazonRDS ....
                    Dimensions=[{'Name':'ServiceName','Value':service},{'Name':'Currency','Value':'USD'}]
                )
            return response['Datapoints'][0]['Maximum']
        except:
            return "ErrorLib - Not charges yet."
            
    # Convert bytes to ?
    def bytes_to(self,bytes,to,bsize=1024):
        try:
            convertOptions = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
            newType = float(bytes)
            for i in range(convertOptions[to]):
                newType = newType / bsize
            return(newType)
        except:
            return "ErrorLib - Can't convert bytes to "+to

    # Return chart from cloudwatch
    def chart(self,region,id,metric,unit):
        try:
            chargeClient = self.connect_client(region,'cloudwatch')
            response = chargeClient.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName=metric,
                    StartTime=datetime.datetime.now() - datetime.timedelta(hours=1),
                    EndTime=datetime.datetime.now(),
                    Period=300,
                    Statistics=['Maximum'],
                    Dimensions=[{'Name':'InstanceId','Value':id}],
                    Unit=unit
                )
            dataChart = {}
            for endpoint in response['Datapoints']:
                if unit == "Bytes":
                    dataChart[endpoint['Timestamp'].strftime('%H%M%S')] = [endpoint['Timestamp'].strftime('%H:%M'),self.bytes_to(endpoint['Maximum'],"m")]
                else:
                    dataChart[endpoint['Timestamp'].strftime('%H%M%S')] = [endpoint['Timestamp'].strftime('%H:%M'),endpoint['Maximum']]
            dataX = []
            dateX = []
            for key in sorted(dataChart):
                dateX.append(dataChart[key][0])
                dataX.append(dataChart[key][1])
            custom_style = Style(
              background='transparent',
              opacity='.6',
              opacity_hover='.9',
              transition='400ms ease-in')            
            bar_chart = pygal.Line(width=530, height=320,explicit_size=True, title=metric,x_label_rotation=60,style=custom_style,human_readable=True,pretty_print=True,tooltip_border_radius=10)
            if unit == "Bytes":
                bar_chart.add("MB", dataX)
            elif unit == "Percent":
                bar_chart.add("%", dataX)
            else:
                bar_chart.add(unit, dataX)
            bar_chart.x_labels = dateX
            return bar_chart
        except:
            return "ErrorLib - Can't return chart."

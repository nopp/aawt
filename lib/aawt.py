#
# Amazon AWS Web Tool (AAWT)
#
import ConfigParser,datetime,pprint,boto3,pygal,sys,json,urllib2,re
from calendar import monthrange
from pygal.style import Style

config = ConfigParser.RawConfigParser()
config.read('/etc/aawt/config.cfg')

class Aawt:

    access_key = config.get('conf','accessKey')
    secret_key = config.get('conf','secretKey')

    ebsTypes = {
        'gp2':'Amazon EBS General Purpose SSD (gp2) volumes',
        'io1':'Amazon EBS Provisioned IOPS SSD (io1) volumes',
        'standard':'Amazon EBS Throughput Optimized HDD (st1) volumes',
        'sc1':'Amazon EBS Cold HDD (sc1) volumes'
    }

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

    # Security Group Info
    def sg_info(self,region,id):
        try:
            sgResource = self.connect_resource(region,"ec2")
            return sgResource.SecurityGroup(id)
        except:
            return "ErrorLib - Can't return SG info."
    
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

    # EC2 Price
    def ec2_price_ondemand(self,intanceType,region,os):
        try:
            if os == "Linux":
                url = "http://a0.awsstatic.com/pricing/1/ec2/linux-od.min.js"
            elif os == "Windows":
                url = "http://a0.awsstatic.com/pricing/1/ec2/mswin-od.min.js"

            fh = urllib2.urlopen(url).read()

            # Prepare JS to use on AAWT :) "little hammers"
            resub = fh[fh.index("(") + 1:fh.rindex(")")]
            resub = re.sub(r'{+',r'{"',resub)
            resub = re.sub(r':',r'":',resub)
            resub = re.sub(r',',r',"',resub)
            resub = re.sub(r':0.01,',r':"0.01",',resub)
            resub = re.sub(r',"{',r',{',resub)
            resub = re.sub(r',""',r',"',resub)

            dataJson = json.loads(resub)

            for regions in dataJson['config']['regions']:
                if regions['region'] == region:
                    for ec2 in regions['instanceTypes'][0]['sizes']:
                        if ec2['size'] == intanceType:
                            return float(ec2['valueColumns'][0]['prices']['USD'])
        except:
            return "ErrorLib - Can't return EC2 price."

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

    # EBS Info
    def ebs_info(self,region,id):
        try:
            ebsResource = self.connect_resource(region,"ec2")
            return ebsResource.Volume(id)
        except:
            return "ErrorLib - Can't return EBS info."

    # EBS Price
    def ebs_price_ondemand(self,ebsType,region,size):
        try:
            url = "http://a0.awsstatic.com/pricing/1/ebs/pricing-ebs.min.js"

            fh = urllib2.urlopen(url).read()

            # Prepare JS to use on AAWT :) "little hammers"
            resub = fh[fh.index("(") + 1:fh.rindex(")")]
            resub = re.sub(r'{+',r'{"',resub)
            resub = re.sub(r':',r'":',resub)
            resub = re.sub(r',',r',"',resub)
            resub = re.sub(r':0.01,',r':"0.01",',resub)
            resub = re.sub(r',"{',r',{',resub)

            dataJson = json.loads(resub)

            for region in dataJson['config']['regions']:
                if region['region'] == "sa-east-1":
                    for vol in region['types']:
                        if vol['name'] == self.ebsTypes[ebsType]:
                            return float(vol['values'][0]['prices']['USD'])*int(size)
        except:
            return "ErrorLib - Can't return EBS price."

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
    def chart(self,region,id,metric,unit,statopt,opt):
        dimensions = {'EC2':'InstanceId','ELB':'LoadBalancerName','RDS':'DBInstanceIdentifier'}
        try:
            chartClient = self.connect_client(region,'cloudwatch')
            response = chartClient.get_metric_statistics(
                Namespace='AWS/'+opt,
                MetricName=metric,
                StartTime=datetime.datetime.now() - datetime.timedelta(hours=1),
                EndTime=datetime.datetime.now(),
                Period=300,
                Statistics=['Average','Sum','Maximum'],
                Dimensions=[{'Name':dimensions[opt],'Value':id}],
                Unit=unit
            )            
            dataChart = {}
            for endpoint in response['Datapoints']:
                if unit == "Bytes":
                    dataChart[endpoint['Timestamp'].strftime('%H%M%S')] = [endpoint['Timestamp'].strftime('%H:%M'),round(self.bytes_to(endpoint['Average'],"m"),2)]
                else:
                    dataChart[endpoint['Timestamp'].strftime('%H%M%S')] = [endpoint['Timestamp'].strftime('%H:%M'),round(endpoint[statopt],2)]
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

    # CloudTrail
    def cloudtrail_listAll(self,region):
        try:
            cloudtrailClient = self.connect_client(region,"cloudtrail")
            return cloudtrailClient.lookup_events()['Events']
        except:
            return "ErrorLib - Can't list CloudTrail."

    # S3
    def s3_listAll(self):
        try:
            s3Client = self.connect_client("","s3")
            return s3Client.list_buckets()['Buckets']
        except:
            return "ErrorLib - Can't list S3."

    # S3 Info
    def s3_info(self,name):
        try:
            s3 = {}
            s3Client = self.connect_client("","s3")
            s3['Location'] = s3Client.get_bucket_location(Bucket=name)['LocationConstraint']
            s3Resource = self.connect_resource(s3['Location'],"s3")        
            s3['Objects'] = s3Client.list_objects(Bucket=name)
            s3['CreatedAt'] = s3Resource.Bucket(name).creation_date
            return s3
        except:
            return "ErrorLib - Can't return S3 info."
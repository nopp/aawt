#
# Amazon AWS Web Tool (AAWT)
#
import math,logging,ConfigParser,os,time,urllib,base64
from flask import *
from lib.aawt import *

config = ConfigParser.RawConfigParser()
config.read('/etc/aawt/config.cfg')

app = Flask(__name__)
app.secret_key = 'BYG>.L*((*$jj2h>#'

aawt = Aawt()

regions = {
    'us-east-1':'US East (N. Virginia)',
    'us-west-1':'US West (N. California)',
    'us-west-2':'US West (Oregon)',
    'eu-west-1':'EU (Ireland)',
    'eu-central-1':'EU (Frankfurt)',
    'ap-northeast-1':'Asia Pacific (Tokyo)',
    'ap-northeast-2':'Asia Pacific (Seoul)',
    'ap-southeast-1':'Asia Pacific (Singapore)',
    'ap-southeast-2':'Asia Pacific (Sydney)',
    'sa-east-1':'South America (Sao Paulo)'
}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',menu=regions), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html',menu=regions), 500

# EC2 List All
@app.route("/ec2/<region>",methods=['GET'])
def ec2(region):
    try:
        if aawt.charge_service('AmazonEC2') == "ErrorLib - Not charges yet.":
            charge = "Not charges yet."
        else:
            charge = format(aawt.charge_service('AmazonEC2'), ',.2f')
        return render_template('ec2.html',results=aawt.ec2_listAll(region),region=region,aawt=aawt,charge=charge,menu=regions)
    except:
	print "ErrorFlask - Can't list all EC2."

# EC2 Info
@app.route("/ec2info/<region>/<id>",methods=['GET'])
def ec2Info(region,id):
    try:
        info = aawt.ec2_info(region,id,"")
	totalVolStandard = 0
	totalVolGp2 = 0
	totalVolIo1 = 0
	totalVol = 0
	for vol in aawt.ec2_info(region,id,"").volumes.all():
	    totalVol = totalVol+vol.size
	    if vol.volume_type == "gp2":
		totalVolGp2 = totalVolGp2+vol.size
	    if vol.volume_type == "standard":
		totalVolStandard = totalVolStandard+vol.size
	    if vol.volume_type == "io1":
		totalVolIo1 = totalVolIo1+vol.size
	hoursOfMonth = monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]*24
        screen = None
        if info.virtualization_type != "paravirtual":
            screen = aawt.connect_client(region,"ec2").get_console_screenshot(InstanceId=id,WakeUp=True)['ImageData']
	return render_template('ec2info.html',region=region,id=id,info=info,totalvol=totalVol,totalvolstandard=totalVolStandard,totalvolgp2=totalVolGp2,totalvolio1=totalVolIo1,aawt=aawt,menu=regions,hours=hoursOfMonth,screen=screen)
    except:
	print "ErrorFlask - Can't return EC2 info."

# EC2 Charts
@app.route("/ec2charts/<region>/<id>",methods=['GET'])
def ec2Charts(region,id):
    try:
        cpuChart = aawt.chart(region,id,"CPUUtilization","Percent","Maximum","EC2").render(is_unicode=True)
        networkInChart = aawt.chart(region,id,"NetworkIn","Bytes","Average","EC2").render(is_unicode=True)
        networkOutChart = aawt.chart(region,id,"NetworkOut","Bytes","Average","EC2").render(is_unicode=True)
        return render_template('ec2charts.html',region=region,id=id,info=aawt.ec2_info(region,id,""),aawt=aawt,cpuChart=cpuChart,networkInChart=networkInChart,networkOutChart=networkOutChart,menu=regions)
    except:
        print "ErrorFlask - Can't return EC2 charts."

# RDS List All
@app.route("/rds/<region>",methods=['GET'])
def rds(region):
    try:
	if aawt.charge_service('AmazonRDS') == "ErrorLib - Not charges yet.":
	    charge = "Not charges yet."
	else:
	    charge = format(aawt.charge_service('AmazonRDS'), ',.2f')
	return render_template('rds.html',results=aawt.rds_listAll(region),region=region,charge=charge,menu=regions)
    except:
	print "ErrorFlask - Can't list all RDS."

# RDS Charts
@app.route("/rdscharts/<region>/<name>",methods=['GET'])
def rdsCharts(region,name):
    try:
	cpuChart = aawt.chart(region,name,"CPUUtilization","Percent","Maximum","RDS").render(is_unicode=True)
	connectionsChart = aawt.chart(region,name,"DatabaseConnections","Count","Average","RDS").render(is_unicode=True)
	return render_template('rdscharts.html',region=region,name=name,aawt=aawt,cpuChart=cpuChart,connectionsChart=connectionsChart,menu=regions)
    except:
	print "ErrorFlask - Can't return RDS charts."

# ELB List All
@app.route("/elb/<region>",methods=['GET'])
def elb(region):
    try:
        return render_template('elb.html',results=aawt.elb_listAll(region),region=region,aawt=aawt,menu=regions)
    except:
        print "ErrorFlask - Can't list all ELB."

# ELB Charts
@app.route("/elbcharts/<region>/<id>",methods=['GET'])
def elbCharts(region,id):
    try:
	latencyChart = aawt.chart(region,id,"Latency","Seconds","Average","ELB").render(is_unicode=True)
	requestsChart = aawt.chart(region,id,"RequestCount","Count","Sum","ELB").render(is_unicode=True)
	return render_template('elbcharts.html',region=region,id=id,aawt=aawt,latencyChart=latencyChart,requestsChart=requestsChart,menu=regions)
    except:
	print "ErrorFlask - Can't return ELB charts."

# IAM List All
@app.route("/iam")
def iam():
    try:
	return render_template('iam.html',results=aawt.iam_listAll(),menu=regions)
    except:
	print "Error - Can't list all users"

# EC2 List all reserved
@app.route("/ec2r/<region>",methods=['GET'])
def ec2r(region):
    try:
	rtn,total = aawt.ec2r_listAll(region)
	return render_template('ec2r.html',results=rtn,total=total,region=region,menu=regions)
    except:
	print "ErrorFlask - Can't list all EC2 reserved."

# EBS List all
@app.route("/ebs/<region>",methods=['GET'])
def ebs(region):
    try:
	rtn,total = aawt.ebs_listAll(region)
	return render_template('ebs.html',results=rtn,region=region,total=total,aawt=aawt,menu=regions)
    except:
	print "ErrorFlask - Can't list all ebs."

# DynamoDB
@app.route("/dynamodb/<region>",methods=['GET'])
def dynamodb(region):
    try:
        return render_template('dynamodb.html',results=aawt.dynamodb_listAll(region),aawt=aawt,menu=regions,region=region)
    except:
        print "ErrorFlask - Can't list DynamoDB."

# Alerts List all
@app.route("/alerts")
def alerts():
    try:
        return render_template('alerts.html',results=aawt.alerts_listAll(),menu=regions)
    except:
        print "Error - Can't list all alerts"

# Index
@app.route("/")
def index():
    try:
        if aawt.charge_service('',"total") == "ErrorLib - Not charges yet.":
	    charge = "Not charges yet."
        else:
            charge = format(aawt.charge_service('',"total"), ',.2f')
        return render_template('index.html',menu=regions,charge=charge,aawt=aawt)
    except:
        print "ErrorFlask - Can't render index."

if __name__ == '__main__':
    logging.basicConfig(filename='aawt.log',level=logging.INFO)
    app.run(host=str(config.get('conf','ip')),port=int(config.get('conf','port')))

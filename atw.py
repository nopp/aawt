#
# ATW - AWS Tool Web
#
import math
import logging
import ConfigParser
from flask import *
from lib.atw import *

config = ConfigParser.RawConfigParser()
config.read('/etc/atw/config.cfg')

app = Flask(__name__)
app.secret_key = 'BYG>.L*((*$jj2h>#'

atw = Atw()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',menu=atw.menu()), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html',menu=atw.menu()), 500

# EC2 List All
@app.route("/ec2/<region>",methods=['GET'])
def ec2(region):
	try:
		if atw.charge_service('AmazonEC2') == "ErrorLib - Not charges yet.":
			charge = "Not charges yet."
		else:
			charge = format(atw.charge_service('AmazonEC2'), ',.2f')
		return render_template('ec2.html',results=atw.ec2_listAll(region),region=region,atw=atw,charge=charge,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all EC2."

# EC2 Info
@app.route("/ec2info/<region>/<id>",methods=['GET'])
def ec2Info(region,id):
	try:
		return render_template('ec2info.html',region=region,id=id,info=atw.ec2_info(region,id,""),atw=atw,menu=atw.menu())
	except:
		print "ErrorFlask - Can't return EC2 info."

# EC2 Charts
@app.route("/ec2charts/<region>/<id>",methods=['GET'])
def ec2Charts(region,id):
	try:
		cpuChart = atw.chart(region,id,"CPUUtilization","Percent","Maximum","EC2").render(is_unicode=True)
		networkInChart = atw.chart(region,id,"NetworkIn","Bytes","Average","EC2").render(is_unicode=True)
		networkOutChart = atw.chart(region,id,"NetworkOut","Bytes","Average","EC2").render(is_unicode=True)
		return render_template('ec2charts.html',region=region,id=id,info=atw.ec2_info(region,id,""),atw=atw,cpuChart=cpuChart,networkInChart=networkInChart,networkOutChart=networkOutChart,menu=atw.menu())
	except:
		print "ErrorFlask - Can't return EC2 charts."

# RDS List All
@app.route("/rds/<region>",methods=['GET'])
def rds(region):
	try:
		if atw.charge_service('AmazonRDS') == "ErrorLib - Not charges yet.":
			charge = "Not charges yet."
		else:
			charge = format(atw.charge_service('AmazonRDS'), ',.2f')
		return render_template('rds.html',results=atw.rds_listAll(region),region=region,charge=charge,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all RDS."

# RDS Charts
@app.route("/rdscharts/<region>/<name>",methods=['GET'])
def rdsCharts(region,name):
	try:
		cpuChart = atw.chart(region,name,"CPUUtilization","Percent","Maximum","RDS").render(is_unicode=True)
		connectionsChart = atw.chart(region,name,"DatabaseConnections","Count","Average","RDS").render(is_unicode=True)
		return render_template('rdscharts.html',region=region,name=name,atw=atw,cpuChart=cpuChart,connectionsChart=connectionsChart,menu=atw.menu())
	except:
		print "ErrorFlask - Can't return RDS charts."

# ELB List All
@app.route("/elb/<region>",methods=['GET'])
def elb(region):
	try:
		return render_template('elb.html',results=atw.elb_listAll(region),region=region,atw=atw,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all ELB."

# ELB Charts
@app.route("/elbcharts/<region>/<id>",methods=['GET'])
def elbCharts(region,id):
	try:
		latencyChart = atw.chart(region,id,"Latency","Seconds","Average","ELB").render(is_unicode=True)
		requestsChart = atw.chart(region,id,"RequestCount","Count","Sum","ELB").render(is_unicode=True)
		return render_template('elbcharts.html',region=region,id=id,atw=atw,latencyChart=latencyChart,requestsChart=requestsChart,menu=atw.menu())
	except:
		print "ErrorFlask - Can't return ELB charts."

# IAM List All
@app.route("/iam")
def iam():
	try:
		return render_template('iam.html',results=atw.iam_listAll(),menu=atw.menu())
	except:
		print "Error - Can't list all users"

# EC2 List all reserved
@app.route("/ec2r/<region>",methods=['GET'])
def ec2r(region):
	try:
		rtn,total = atw.ec2r_listAll(region)
		return render_template('ec2r.html',results=rtn,total=total,region=region,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all EC2 reserved."

# EBS List all
@app.route("/ebs/<region>",methods=['GET'])
def ebs(region):
	try:
		rtn,total = atw.ebs_listAll(region)
		return render_template('ebs.html',results=rtn,region=region,total=total,atw=atw,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all ebs."

# CloudTrail
@app.route("/cloudtrail/<region>",methods=['GET'])
def cloudtrail(region):
	try:
		return render_template('cloudtrail.html',results=atw.cloudtrail_listAll(region),region=region,menu=atw.menu())
	except:		
		print "ErrorFlask - Can't list CloudTrail."

# S3
@app.route("/s3",methods=['GET'])
def s3():
	try:
		return render_template('s3.html',results=atw.s3_listAll(),atw=atw,menu=atw.menu())
	except:		
		print "ErrorFlask - Can't list S3."

# S3 Info
@app.route("/s3info/<name>",methods=['GET'])
def s3Info(name):
	try:
		return render_template('s3info.html',name=name,s3info=atw.s3_info(name),menu=atw.menu())
	except:
		print "ErrorFlask - Can't return S3 info."

# Index
@app.route("/")
def index():
	try:
		if atw.charge_service('',"total") == "ErrorLib - Not charges yet.":
			charge = "Not charges yet."
		else:
			charge = format(atw.charge_service('',"total"), ',.2f')
		return render_template('index.html',menu=atw.menu(),charge=charge,atw=atw)
	except:
		print "ErrorFlask - Can't render index."

if __name__ == '__main__':
	#logging.basicConfig(filename='atw.log',level=logging.INFO)
	app.run(host=str(config.get('conf','ip')),port=int(config.get('conf','port')),debug=True)

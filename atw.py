#
# ATW - AWS Tool Web
#
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
		return render_template('ec2.html',results=atw.ec2_listAll(region),region=region,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all EC2."

# RDS List All
@app.route("/rds/<region>",methods=['GET'])
def rds(region):
	try:
		return render_template('rds.html',results=atw.rds_listAll(region),region=region,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all RDS."

# ELB List All
@app.route("/elb/<region>",methods=['GET']) 
def elb(region):
	try:
		return render_template('elb.html',results=atw.elb_listAll(region),region=region,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all ELB."

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
		return render_template('ebs.html',results=rtn,region=region,total=total,menu=atw.menu())
	except:
		print "ErrorFlask - Can't list all ebs."

@app.route("/")
def index():
	return render_template('index.html',menu=atw.menu(),atw=atw)

if __name__ == '__main__':
	logging.basicConfig(filename='atw.log',level=logging.INFO)
	app.run(host=str(config.get('conf','ip')),port=int(config.get('conf','port')))
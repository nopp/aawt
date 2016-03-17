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

# EC2 List All
@app.route("/ec2/<region>",methods=['GET'])
def ec2(region):
	try:	
		atw = Atw()
		rtn = atw.ec2_listAll(region)
		return render_template('ec2.html',results=rtn,region=region)
	except:
		print "Error - Can't list all EC2"

# RDS List All
@app.route("/rds/<region>",methods=['GET'])
def rds(region):
	try:
		atw = Atw()
		rtn = atw.rds_listAll(region)
		return render_template('rds.html',results=rtn,region=region)
	except:
		print "Error - Can't list all RDS"

@app.route("/")
def index():
	atw = Atw()
#	ec2TotalSP = atw.ec2_total("sa-east-1")
#	ec2TotalVirginia = atw.ec2_total("us-east-1")
#	ebsTotalSizeSP,ebsTotalSP = atw.ebs_total("sa-east-1")
#	ebsTotalSizeVirginia,ebsTotalVirginia = atw.ebs_total("us-east-1")
#	return render_template('index.html',ebsTotalSP=ebsTotalSP,ebsTotalVirginia=ebsTotalVirginia,ec2TotalSP=ec2TotalSP,ec2TotalVirginia=ec2TotalVirginia,ebsTotalSizeSP=ebsTotalSizeSP,ebsTotalSizeVirginia=ebsTotalSizeVirginia)
	return render_template('index.html')

if __name__ == '__main__':
	logging.basicConfig(filename='/var/log/atw/atw.log',level=logging.INFO)
	app.run(host=str(config.get('conf','ip')),port=int(config.get('conf','port')))

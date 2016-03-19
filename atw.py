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

# EC2 List All
@app.route("/ec2/<region>",methods=['GET']) 
def ec2(region):
	try:	
		return render_template('ec2.html',results=atw.ec2_listAll(region),region=region,menu=atw.menu())
	except:
		print "Error - Can't list all EC2"

# RDS List All
@app.route("/rds/<region>",methods=['GET'])
def rds(region):
	try:
		return render_template('rds.html',results=atw.rds_listAll(region),region=region,menu=atw.menu())
	except:
		print "Error - Can't list all RDS"

@app.route("/")
def index():
	return render_template('index.html',menu=atw.menu())

if __name__ == '__main__':
	logging.basicConfig(filename='atw.log',level=logging.INFO)
	app.run(host=str(config.get('conf','ip')),port=int(config.get('conf','port')))

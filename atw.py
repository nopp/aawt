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
app.secret_key = 'BYG>.L*((*$jjkh>>'

# EC2 List All
@app.route("/")
def index():
	try:	
		atw = Atw()
		rtn = atw.ec2_listAll()
		return render_template('index.html',results=rtn)
	except:
		print "Error - Can't list all EC2"

if __name__ == '__main__':
	logging.basicConfig(filename='/var/log/atw/atw.log',level=logging.INFO)
	app.run(host=str(config.get('conf','ip')),port=int(config.get('conf','port')))
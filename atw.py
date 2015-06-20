#
# ATW - AWS Tool Web
#
import ConfigParser
from flask import *
from lib.atw import *

config = ConfigParser.RawConfigParser()
config.read('/etc/atw/config.cfg')

app = Flask(__name__)
app.secret_key = 'BYG>.L*((*$jjkh>>'

# Index
@app.route("/")
def index():
	return render_template('index.html')

# EC2 Search by IP
@app.route("/ec2_search_ip")
def ec2_search_ip():	
	return render_template('ec2_search_ip.html')

@app.route("/ec2SearchIP", methods=['POST'])
def ec2ip():
	try:
		if request.method == 'POST':	
			atw = Atw()
			rtn = atw.ec2_searchByIP(request.form['ip'],request.form['iptype'])
			total = len(rtn)
		return render_template('ec2_search_ip.html',results=rtn,total=total,ip=request.form['ip'],type=request.form['iptype'])
	except:
		print "Error - Can't search EC2 by IP"

@app.route("/ec2_list_all")
def ec2_list_all():
	try:	
		atw = Atw()
		rtn = atw.ec2_listAll()
		total = len(rtn)
		return render_template('ec2_list_all.html',results=rtn,total=total)
	except:
		print "Error - Can't list all EC2"

# EC2 Search by TAG
@app.route("/ec2_search_tag")
def ec2_search_tag():	
	return render_template('ec2_search_tag.html')

@app.route("/ec2SearchTAG", methods=['POST'])
def ec2tag():
	try:
		if request.method == 'POST':	
			atw = Atw()
			rtn = atw.ec2_searchByTAG(request.form['tagKey'],request.form['tagValue'])
			total = len(rtn)
		return render_template('ec2_search_tag.html',results=rtn,total=total,key=request.form['tagKey'],value=request.form['tagValue'])
	except:
		print "Error - Can't search EC2 by TAG"

if __name__ == '__main__':
	app.run(host=str(config.get('conf','ip')),port=int(config.get('conf','port')),debug=True)	
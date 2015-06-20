#
# ATW - AWS Tool Web
#
from flask import *
from lib.atw import *

app = Flask(__name__)
app.secret_key = 'BYG>.L*((*$jjkh>>'

# Index
@app.route("/")
def index():
	return render_template('home.html')

# EC2 SearchByIP
@app.route("/ec2_searchByIP", methods=['POST'])
def ec2_searchByIP():
	try:
		if request.method == 'POST':	
			atw = Atw()
			rtn = atw.searchByIP(request.form['ip'],request.form['iptype'])
			total = len(rtn)
		return render_template('result.html',results=rtn,total=total)
	except:
		print "Error - Can't search EC2 by IP"

# EC2 SearchByTAG
@app.route("/ec2_searchByTAG", methods=['POST'])
def ec2_searchByTAG():
	try:
		if request.method == 'POST':	
			atw = Atw()
			rtn = atw.searchByTAG(request.form['tagKey'],request.form['tagValue'])
			total = len(rtn)
		return render_template('result.html',results=rtn,total=total)
	except:
		print "Error - Can'tsearch EC2 by TAG"

if __name__ == '__main__':
	app.run(host='10.211.55.18',port=80,debug=True)	
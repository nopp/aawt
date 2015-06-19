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
	if request.method == 'POST':	
		atw = Atw()
		if request.form['iptype'] == "public":
			rtn = atw.searchByPIP(request.form['ip'])
		else:
			rtn = atw.searchByPrIP(request.form['ip'])
	return render_template('result.html',results=rtn)

# EC2 SearchByTAG
@app.route("/ec2_searchByTAG", methods=['POST'])
def ec2_searchByTAG():
	if request.method == 'POST':	
		atw = Atw()
		rtn = atw.searchByTAG(request.form['tagKey'],request.form['tagValue'])
		total = len(rtn)
	return render_template('result.html',results=rtn,total=total)

# EC2 List 
@app.route('/ec2_list')
def ec2_list():
	return render_template('addHost.html')

if __name__ == '__main__':
	app.run(host='172.173.4.74',port=8082,debug=True)

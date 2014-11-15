#
# Docking - Docker manager web
#
import logging
import json
from flask import *
from lib.docking import *

app = Flask(__name__)
app.secret_key = 'aYG>.k*((*@jjkh>>'

# Security
def verifyAdmin():
	if "docking_auth" in session:
		if session['docking_group'] == "admin":
			return True
		else:
			return False
	else:
		return False

# Login
@app.route("/login")
def login():
	return render_template('login.html')

# Verify login
@app.route("/verify", methods=['POST'])
def verify():
	if request.method == 'POST':
		docking = Docking()
		if docking.verifyLogin(request.form['login'],request.form['password']):
			session['docking_auth'] = request.form['login']
			session['docking_group'] = docking.returnGroup(request.form['login'])
			if docking.returnGroup(request.form['login']) == "dev":
				session['docking_host'] = docking.returnTeamInfo(request.form['login'],"id_host")
			return redirect(url_for('index'))
		else:
			flash("Login error!")
			return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
	session.pop('docking_auth', None)
	session.pop('docking_group', None)
	return redirect(url_for('index'))

# Index
@app.route("/")
def index():
	if "docking_auth" in session:
		docking = Docking()
		if session['docking_group'] == "admin":
			info = []
			info.append(docking.dockingInfo("hosts"))
			info.append(docking.dockingInfo("teams"))
			info.append(docking.dockingInfo("containers"))
			return render_template('home.html', clt=docking.returnHosts(), infodocking=info)
		else:
			dockerHost = docking.returnHostById(docking.returnTeamInfo(session['docking_auth'],"id_host"))[2]
			maxMemory = docking.returnTeamInfo(session['docking_auth'],"max_memory")
			idTeam = docking.returnTeamInfo(session['docking_auth'],"id")
			return render_template('home.html', clt=docking.returnContainersTeam(idTeam), mm=maxMemory, c=0, host=dockerHost)
	else:
		return redirect(url_for('login'))

# Version
@app.route("/version/<dockerHost>", methods=['GET'])
def version(dockerHost):
	if "docking_auth" in session:
		if request.method == 'GET':
			dApi = dockerApi()
			rtn = dApi.docker_version(dockerHost)
			return rtn
	else:
		flash("Please sign in!")
		return redirect(url_for('login'))

# Info
@app.route("/info/<dockerHost>", methods=['GET'])
def info(dockerHost):
	if(verifyAdmin()):
		if request.method == 'GET':
			dApi = dockerApi()
			rtn = dApi.docker_info(dockerHost)
			return rtn
	else:
		flash("Please sign in!")
		return redirect(url_for('login'))

# Register new host
@app.route('/rh')
def rh():
	if(verifyAdmin()):
		return render_template('addHost.html')
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/register_host', methods=['POST'])
def registerHost():
	if(verifyAdmin()):
		if request.method == 'POST':
			docking = Docking()
			rtn = docking.addHost(request.form['name'],request.form['ip'],request.form['port'],request.form['max_memory'])
			flash(rtn)
			return redirect(url_for('index'))
		else:
			flash("Restricted area!")
			return redirect(url_for('login'))

# Create team
@app.route('/ct')
def ct():
	if(verifyAdmin()):
		return render_template('addTeam.html')
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

@app.route('/create_team', methods=['POST'])
def createTeam():
	if(verifyAdmin()):
		if request.method == 'POST':
			docking = Docking()
			rtn = docking.addTeam(request.form['name'],request.form['login'],request.form['pass'],request.form['group'],request.form['max_memory'])
			flash(rtn)
			return redirect(url_for('index'))
	else:
		flash("Restricted area!")
		return redirect(url_for('login'))

# Containers
@app.route("/containers/<dockerHost>", methods=['GET'])
def containers(dockerHost):
	if "docking_auth" in session:
		if request.method == 'GET':
			dApi = dockerApi()
			rtn = dApi.docker_containers(dockerHost)
			return rtn
	else:
		flash("Please sign in!")
		return redirect(url_for('login'))

# Container Info
@app.route("/container/<dockerHost>/<idContainer>", methods=['GET'])
def containerInfo(dockerHost,idContainer):
	if "docking_auth" in session:
		if request.method == 'GET':
			dApi = dockerApi()
			rtn = dApi.docker_container_info(dockerHost,idContainer)
			return rtn
	else:
		flash("Please sign in!")
		return redirect(url_for('login'))

# Container start test
@app.route("/start", methods=['POST'])
def containerStart():
	if "docking_auth" in session:
		if request.method == 'POST':
			dApi = dockerApi()
			rtn = dApi.docker_container_start(request.form['dockerHost'],request.form['idContainer'])
			return rtn
	else:
		flash("Please sign in!")
		return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8282,debug=True)

#
# Docking - Web Docker GUI
#
import logging
import json
from flask import *
from lib.docker_api import *

app = Flask(__name__)
app.secret_key = 'aYG>.k*((*@jjkh>>'

# Index
@app.route("/")
def index():
	return "Docking - Web Docker GUI"

# Version
@app.route("/version/<dockerHost>", methods=['GET'])
def version(dockerHost):
	if request.method == 'GET':
		dApi = dockerApi()
		rtn = dApi.docker_version(dockerHost)
		return rtn

# Info
@app.route("/info/<dockerHost>", methods=['GET'])
def info(dockerHost):
	if request.method == 'GET':
		dApi = dockerApi()
		rtn = dApi.docker_info(dockerHost)
		return rtn

# Containers
@app.route("/containers/<dockerHost>", methods=['GET'])
def containers(dockerHost):
	if request.method == 'GET':
		dApi = dockerApi()
		rtn = dApi.docker_containers(dockerHost)
		return rtn

# Container Info
@app.route("/container/<dockerHost>/<idContainer>", methods=['GET'])
def containerInfo(dockerHost,idContainer):
	if request.method == 'GET':
		dApi = dockerApi()
		rtn = dApi.docker_container_info(dockerHost,idContainer)
		return rtn

# Container start test
@app.route("/start", methods=['POST'])
def containerStart():
	if request.method == 'POST':
		dApi = dockerApi()
		rtn = dApi.docker_container_start(request.form['dockerHost'],request.form['idContainer'])
		return rtn

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8282,debug=True)

#
# Docking - Web Docker GUI
#
import json
import urllib2
from urllib2 import Request, urlopen, URLError

class dockerApi():

	def urlRequest(self,dockerAgent,action):
		uName = "carlos"
		pWord = "loke99"
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		try:
			req = urllib2.Request('http://'+str(dockerAgent)+'/'+str(action))
			req.add_header('Accept', 'application/json')
			req.add_header("Content-type", "application/x-www-form-urlencoded")
			req.add_header('Authorization', userData)
			return req
		except URLError, e:
			return e.reason

	def docker_version(self,dockerHost):
		try:
			req = self.urlRequest(dockerHost,"version")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	def docker_containers(self,dockerHost):
		try:
			req = self.urlRequest(dockerHost,"containers/json?all")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	def docker_container_info(self,dockerHost,idContainer):
		try:
			req = self.urlRequest(dockerHost,"containers/"+idContainer+"/json")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

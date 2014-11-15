#
# Docking - Docker manager web
#
import json
import urllib2
from urllib2 import Request, urlopen, URLError

class dockerApi():

	def urlRequest(self,dockerAgent,action,mtd=None):
		uName = "userhttp"
		pWord = "passhttp"
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		try:
			if mtd == "POST":
				req = urllib2.Request('http://'+dockerAgent+'/'+action)
				req.get_method = lambda: 'POST'
				req.add_header('Accept', 'application/json')
				req.add_header("Content-type", "application/x-www-form-urlencoded")
				req.add_header('Authorization', userData)
				return req
			else:
				req = urllib2.Request('http://'+dockerAgent+'/'+action)
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

	def docker_info(self,dockerHost):
		try:
			req = self.urlRequest(dockerHost,"info")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	# Container methods

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

	def docker_container_start(self,dockerHost,idContainer):
		try:
			req = self.urlRequest(dockerHost,"containers/"+idContainer+"/start","POST")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	def docker_container_stop(self,dockerHost,idContainer):
		try:
			req = self.urlRequest(dockerHost,"containers/"+idContainer+"/stop","POST")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

	def docker_container_restart(self,dockerHost,idContainer):
		try:
			req = self.urlRequest(dockerHost,"containers/"+idContainer+"/restart","POST")
			rtn = urllib2.urlopen(req,timeout = 2)
			return rtn.read()
		except URLError, e:
			return e.reason

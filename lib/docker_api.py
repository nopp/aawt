#
# Docking - Web Docker GUI
#
import json
import urllib2
from urllib2 import Request, urlopen, URLError

class dockerApi():

	def urlRequest(self,dockerAgent,action,extra=None,mtd=None,domain=None):
		uName = "carlos"
		pWord = "loke99"
		userData = "Basic " + (uName + ":" + pWord).encode("base64").rstrip()
		if (extra != None):
			try:
				# Type of method (POST/PUT)
				if mtd == "POST":
					if action == "ban":
						req = urllib2.Request('http://'+dockerAgent+'/'+action+'/'+str(extra))
						req.get_method = lambda: 'POST'
					else:
						req = urllib2.Request('http://'+dockerAgent+'/'+action+'/',str(extra))
						req.get_method = lambda: 'POST'
				elif mtd == "PUT":
					req = urllib2.Request('http://'+dockerAgent+'/'+action+'/'+str(extra), data=str(extra))
					req.get_method = lambda: 'PUT'
				else:
					req = urllib2.Request('http://'+dockerAgent+'/'+action+'/'+str(extra))
				if domain != None:
					req.add_header('Host', domain)
				req.add_header('Accept', 'application/json')
				req.add_header("Content-type", "application/x-www-form-urlencoded")
				req.add_header('Authorization', userData)
				return req
			except URLError, e:
				return e.reason
		else:
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

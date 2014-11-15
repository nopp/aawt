#
# Docking - Docker manager web
#
import json
import urllib
import MySQLdb
import commands
import ConfigParser
import socket
from urlparse import urlparse
from time import gmtime, strftime

config = ConfigParser.RawConfigParser()
config.read('/etc/docking/config.cfg')

# Docker API
from lib.docker_api import *

class Docking:

	# MySQL connection
	def connect(self):
		mHost = config.get('conf','mysqlHost')
		mUser = config.get('conf','mysqlUser')
		mPass = config.get('conf','mysqlPass')
		mDb = config.get('conf','mysqlDb')
		try:
			con = MySQLdb.connect(host=mHost, user=mUser, passwd=mPass,db=mDb)
			return con
		except:
			return "MySQL connection error!"

	# Verify login
	def verifyLogin(self,login,passwd):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from teams where login = %s and passwd = %s',[login,passwd])
			total = c.fetchone()[0]
			if total == 1:
				c.close()
				return True
			else:
				c.close()
				return False
		except:
			return False

	# Return group from team
	def returnGroup(self,login):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from teams where login = %s',[login])
			total = c.fetchone()[0]
			if total == 1:
				c.execute('select teams.team_group from teams where login = %s',[login])
				if c.fetchone()[0] == "admin":
					userGroup = "admin"
				else:
					userGroup = "dev"
				c.close()
				return userGroup
			else:
				c.close()
				return "User "+login+" doesn't exists!"
		except:
			return "returnGroup - Error!"

	def dockingInfo(self,table):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from '+table)
			total = c.fetchone()[0]
			return total
		except:
			return "vagInfo - MySQL error"

	# Register new host
	def addHost(self,name,ip,port,maxMemory):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from hosts where name = %s',[name])
			total = c.fetchone()[0]
			if total >= 1:
				c.close()
				return "This host "+ip+" has already been added!"
			else:
				c.execute('insert into hosts (name,ip,port,max_memory) values (%s,%s,%s,%s)',[name,ip,port,maxMemory])
				con.commit()
				c.close()
				return "Host "+name+" registered!"
		except:
			return "Error to insert host on MySQL"

	# Create team
	def addTeam(self,name,login,password,group,maxMemory,idHost=1):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from teams where name = %s',[name])
			total = c.fetchone()[0]
			if total >= 1:
				c.close()
				return "This team "+ip+" has already been added!"
			else:
				c.execute('insert into teams (name,login,passwd,team_group,max_memory,id_host) values (%s,%s,%s,%s,%s,%s)',[name,login,password,group,maxMemory,idHost])
				con.commit()
				c.close()
				return "Team "+name+" registered!"
		except:
			return "Error to insert team on MySQL"

	# Return hosts
	def returnHosts(self):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from hosts')
			total = c.fetchone()[0]
			if total >= 1:
				hosts = []
				c.execute('select * from hosts order by id DESC')
				for hst in c.fetchall():
					hst = [hst[0],hst[1],hst[2],hst[3],hst[4]]
					hosts.append(hst)
				c.close()
				return hosts
			else:
				return "Please, register a host"
		except:
			return "Error to return hosts on MySQL"

	# Return host by id
	def returnHostById(self,idHost):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from hosts where id = %s',[idHost])
			total = c.fetchone()[0]
			if total >= 1:
				hosts = []
				c.execute('select * from hosts where id = %s',[idHost])
				rtnHost = c.fetchone()
				c.close()
				return rtnHost
			else:
				return "Please, register a host"
		except:
			return "Error to return host on MySQL"

	# Return team info
	def returnTeamInfo(self,loginTeam,info):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from teams where login = %s',[loginTeam])
			total = c.fetchone()[0]
			if total >= 1:
				c.execute('select teams.'+info+' from teams where login = %s',[loginTeam])
				rtnInfo = c.fetchone()[0]
				c.close()
				return rtnInfo
			else:
				return "Please, register a team"
		except:
			return "Error to return team info on MySQL"

	# Return containers from team
	def returnContainersTeam(self,idTeam):
		try:
			con = self.connect()
			c = con.cursor()
			c.execute('select count(*) from containers where id_team = %s',[idTeam])
			total = c.fetchone()[0]
			if total >= 1:
				c.execute('select teams.'+info+' from teams where login = %s',[loginTeam])
				rtnInfo = c.fetchall()
				c.close()
				return rtnInfo
			else:
				return "Your team doesn't have containers yet!"
		except:
			return "Error to return team info on MySQL"

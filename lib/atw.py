#
# ATW - AWS Tool Web
#
import ConfigParser
import boto.ec2
import boto.rds
import sys

config = ConfigParser.RawConfigParser()
config.read('/etc/atw/config.cfg')

class Atw:

	# This is a little hammer, I'll fix this soon :D
	def error(self,message):
		error = []
		eMsg = [message]
		error.append(eMsg)
		return error

	# Connect to EC2
	def ec2_connect(self,region):
		try:
			access_key = config.get('conf','accessKey')
			secret_key = config.get('conf','secretKey')
			conn = boto.ec2.connect_to_region(region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
			return conn
		except:			
			return self.error("Error - can't connect to EC2 (LIB)")

	# Connect to RDS
	def rds_connect(self,region):
		try:
			access_key = config.get('conf','accessKey')
			secret_key = config.get('conf','secretKey')
			conn = boto.rds.connect_to_region(region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
			return conn
		except:
			return self.error("Error - can't connect to RDS (LIB)")

	# Return EC2 Tags
	def returnTags(self,tags):
		ec2Tags = []
		for tagKey,tagValue in tags.iteritems():
			ec2Tags.append(tagKey+":"+tagValue)
		return ec2Tags

	# EC2 List all
	def ec2_listAll(self,region):
		ec2_conn = self.ec2_connect(region)
		try:
			# Filter example:
			# filters = {"private-ip-address": ip}
			# ec2_conn.get_only_instances(filters=filters)
			ec2List = []
			for ec2 in ec2_conn.get_only_instances():
				tagList = self.returnTags(ec2.tags)
				sgList = self.return_ec2SGs(ec2.groups)
				ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state,ec2.placement,tagList,sgList]
				ec2List.append(ec2Vm)
			return ec2List
		except:
			return self.error("Error - Can't list all EC2 (LIB)")

	# Return SGs from EC2
	def return_ec2SGs(self,ec2Groups):
		listSGs = []
		for sg in ec2Groups:
			listSGs.append(sg.name+" ("+sg.id+")")
		return listSGs

	# RDS List all
	def rds_listAll(self,region):
		rds_conn = self.rds_connect(region)
		try:
			rdsList = []
			for rds in rds_conn.get_all_dbinstances():
				rdsInstance = [rds.DBName,rds.engine,rds.master_username,rds.endpoint[0],rds.endpoint[1],rds.status]
				rdsList.append(rdsInstance)
			return rdsList
		except:
			return self.error("Error - Can't list all RDS (LIB)")

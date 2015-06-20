#
# ATW - AWS Tool Web
#
import ConfigParser
import boto.ec2
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

	def ec2_connect(self):
		try:
			access_key = config.get('conf','accessKey')
			secret_key = config.get('conf','secretKey')
			region = config.get('conf','region')
			conn = boto.ec2.connect_to_region(region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
			return conn
		except:			
			return self.error("Error - can't connect to EC2 (LIB)")

	# EC2 Search by IP (Private/Public) 
	def ec2_searchByIP(self,ip,iptype):
		ec2_conn = self.ec2_connect()
		try:
			if iptype == "private":
				filters = {"private-ip-address": ip}
			else:
				filters = {"ip-address": ip}
			ec2List = []
			for ec2 in ec2_conn.get_only_instances(filters=filters):
				ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state]
				ec2List.append(ec2Vm)
			return ec2List
		except:
			return self.error("Error - Can't search EC2 by IP (LIB)")

	# EC2 Search by TAG
	def ec2_searchByTAG(self,tagKey,tagValue):
		ec2_conn = self.ec2_connect()
		try:
			filters = {"tag-key":tagKey,"tag-value":"*"+tagValue+"*"}
			ec2List = []
			for ec2 in ec2_conn.get_only_instances(filters=filters):
				ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state]
				ec2List.append(ec2Vm)
			return ec2List
		except:
			return self.error("Error - Can't search EC2 by TAG (LIB)")

	# EC2 List all
	def ec2_listAll(self):
		ec2_conn = self.ec2_connect()
		try:
			ec2List = []
			for ec2 in ec2_conn.get_only_instances():
				ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state]
				ec2List.append(ec2Vm)
			return ec2List
		except:
			return self.error("Error - Can't list all EC2 (LIB)")

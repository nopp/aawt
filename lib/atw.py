#
# ATW - AWS Tool Web
#
import ConfigParser
import argparse
import boto.ec2
import sys

config = ConfigParser.RawConfigParser()
config.read('/etc/atw/config.cfg')

class Atw:

	region = "sa-east-1"

	def ec2_connect(self):
		try:
			access_key = config.get('conf','accessKey')
			secret_key = config.get('conf','secretKey')
			conn = boto.ec2.connect_to_region(self.region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)
			return conn
		except:
			print "Error - can't connect to EC2 (LIB)"

	# EC2 Search by IP (Private) 
	def searchByPrIP(self,ip):
		ec2_conn = self.ec2_connect()
		try:
			filters = {"private-ip-address": ip}
			ec2List = []
			for ec2 in ec2_conn.get_only_instances(filters=filters):
				ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state]
				ec2List.append(ec2Vm)
			return ec2List
		except:
			print "Error - Can't search EC2 by Private IP (LIB)"

	# EC2 Search by IP (Public)
	def searchByPIP(self,ip):
		ec2_conn = self.ec2_connect()
		try:
			filters = {"ip-address": ip}
			ec2List = []
			for ec2 in ec2_conn.get_only_instances(filters=filters):
				ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state]
				ec2List.append(ec2Vm)
			return ec2List
		except:
			print "Error - Can't search EC2 by Public IP (LIB)"

	# EC2 Search by TAG
	def searchByTAG(self,tagKey,tagValue):
		ec2_conn = self.ec2_connect()
		try:
			filters = {"tag-key":tagKey,"tag-value":"*"+tagValue+"*"}
			ec2List = []
			for ec2 in ec2_conn.get_only_instances(filters=filters):
				ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state]
				ec2List.append(ec2Vm)
			return ec2List
		except:
			print "Error - Can't search EC2 by TAG (LIB)"

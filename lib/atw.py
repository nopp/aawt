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
		access_key = config.get('conf','accessKey')
		secret_key = config.get('conf','secretKey')
		return boto.ec2.connect_to_region(self.region,aws_access_key_id=access_key,aws_secret_access_key=secret_key)

	# EC2 Search by IP (Private) 
	def searchByPrIP(self,ip):
		ec2_conn = self.ec2_connect()
		filters = {"private-ip-address": ip}
		for ec2 in ec2_conn.get_only_instances(filters=filters):
			return ec2.tags['Name']+" "+ec2.id+" "+ec2.private_ip_address+" "+ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType']+" ("+ec2.state+")"

	# EC2 Search by IP (Public)
	def searchByPIP(self,ip):
		ec2_conn = self.ec2_connect()
		filters = {"ip-address": ip}
		ec2List = []
		for ec2 in ec2_conn.get_only_instances(filters=filters):
			ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state]
			ec2List.append(ec2Vm)
		return ec2List

	# EC2 Search by TAG
	def searchByTAG(self,tagKey,tagValue):
		ec2_conn = self.ec2_connect()
		filters = {"tag-key":tagKey,"tag-value":"*"+tagValue+"*"}
		ec2List = []
		for ec2 in ec2_conn.get_only_instances(filters=filters):
			ec2Vm = [ec2.tags['Name'],ec2.id,ec2.private_ip_address,ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType'],ec2.state]
			ec2List.append(ec2Vm)
		return ec2List

	def ec2_list(self):
		ec2_conn = ec2_connect()
		for ec2 in ec2_conn.get_only_instances():
			return ec2.tags['Name']+" "+ec2.id+" "+ec2.private_ip_address+" "+ec2_conn.get_instance_attribute(ec2.id,"instanceType")['instanceType']+" ("+ec2.state+")"

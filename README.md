# Amazon AWS Web Tool (AAWT) discontinued

![Code scanning - action](https://github.com/nopp/aawt/workflows/Code%20scanning%20-%20action/badge.svg)

Features
========
* Cloudfront (simple)
* EC2 (With Charts and Prices)
* EC2 Reserved
* EBS
* ELB (With Charts) Obs:. only classic load balancer
* RDS (With Charts)
* IAM
* DynamoDB
* Alerts

Amazon AWS configuration:
========================
Create an user aawt with access_key and private_key
Attach policy below on aawt user:

	* AmazonEC2ReadOnlyAccess
	* IAMReadOnlyAccess
	* AmazonRDSReadOnlyAccess
	* CloudWatchReadOnlyAccess
	* AmazonDynamoDBReadOnlyAccess
	* CloudFrontReadOnlyAccess
	You need to create an inline policy:	
	{
	    "Version": "2012-10-17",
	    "Statement": [
		{
		    "Effect": "Allow",
		    "Action": [
				"ec2:GetConsoleOutput*",
				"ec2:GetConsoleScreenshot*",
				"health:Describe*"
		    ],
		    "Resource": "*"
		}]
	}
	
You need to enable "Monitor your estimated charges"

* Billing & Cost Management > Preferences > Check "Receive Billing Alerts"

Obs:. this will work some hours later.


RUNNING ON DOCKER
=================

	# docker container run -p 8082:8082 -e akey=yourAccessKey -e skey='yourSecretKey' -d nopp/aawt:1

RUNNING ON SEVER
================
Install
=======
	# yum install python-pip supervisor -y
	# git clone https://github.com/nopp/aawt.git
	# cd aawt
	# pip install -r requirements.txt
	-> configure the application
	# python aawt.py

Configure
=========

	Server:
	=======
	Copy config.cfg to /etc/aawt/config.cfg(and configure it).

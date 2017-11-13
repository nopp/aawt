# Amazon AWS Web Tool (AAWT)

Constantly updated

Features
========
* EC2 (With Charts and Prices)
* EC2 Reserved
* EBS
* ELB (With Charts) Obs:. only classic load balancer
* RDS (With Charts)
* IAM
* DynamoDB
* Alerts

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

	Amazon AWS:
	===========
	Create an user aawt with access_key and private_key
	Attach policy below on aawt user:
	* AmazonEC2ReadOnlyAccess
	* IAMReadOnlyAccess
	* AmazonRDSReadOnlyAccess
	* CloudWatchReadOnlyAccess
	* AmazonDynamoDBReadOnlyAccess
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

Screenshot
==========
![Image Alt](http://i67.tinypic.com/cl1t3.png)
![Image Alt](http://i68.tinypic.com/2yv5rw0.png)
![Image Alt](http://i68.tinypic.com/33uap7s.png)

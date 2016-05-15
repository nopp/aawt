# ATW (AWS Tool Web)

Constantly updated

Required
========
	Python + Flask + Boto3
	
DONE
====
* EC2
* EC2 Reserved
* EBS
* ELB
* RDS
* IAM

Install
=======
	# yum install python-pip -y
	# pip install flask
	# pip install boto3
	# pip install pygal
	# pip install cairosvg
	# git clone https://github.com/nopp/atw.git
	# cd atw
	-> configure the application
	# python atw.py

Configure
=========

	Amazon AWS:
	===========
	Create an user atw with access_key and private_key
	Attach policy below on atw user:
	* AmazonEC2ReadOnlyAccess
	* IAMReadOnlyAccess
	* AmazonRDSReadOnlyAccess
	* CloudWatchReadOnlyAccess
	You need to create an inline policy (getConsoleEC2) to allow method "GetConsoleOutput":
	{
	    "Version": "2012-10-17",
	    "Statement": [
	        {
	            "Effect": "Allow",
	            "Action": "ec2:GetConsoleOutput*",
	            "Resource": "*"
	        }
	    ]
	}
	You need to enable "Monitor your estimated charges"
	* Billing & Cost Management > Preferences > Check "Receive Billing Alerts"
	Obs:. this will work some hours later.

	Server:
	=======
	Create a file /etc/atw/config.cfg with:
		[conf]
		regions = sa-east-1:Sao Paulo,us-east-1:Virginia # You need to use this "pattern"
		accessKey = yourAccessKeyWithReadOnly
		secretKey = yourPrivateKeyWithReadOnly
		ip = ipOfYourATWServer
		port = portOfYourATWServer

Screenshot
==========
![Image Alt](http://i66.tinypic.com/4tr2o4.png)
![Image Alt](http://i66.tinypic.com/9rkebq.png)
![Image Alt](http://i63.tinypic.com/99oynp.png)

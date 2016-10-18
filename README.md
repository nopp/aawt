# Amazon AWS Web Tool (AAWT)

Constantly updated
	
FEATURES
========
* EC2 (With Charts and Prices)
* EC2 Reserved
* EBS
* ELB (With Charts)
* RDS (With Charts)
* IAM
* CloudTrail
* S3

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

	Amazon AWS:
	===========
	Create an user aawt with access_key and private_key
	Attach policy below on aawt user:
	* AmazonEC2ReadOnlyAccess
	* IAMReadOnlyAccess
	* AmazonRDSReadOnlyAccess
	* CloudWatchReadOnlyAccess
	* AmazonS3ReadOnlyAccess
	* AWSCloudTrailReadOnlyAccess
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
	Create a file /etc/aawt/config.cfg with:
	[conf]
	accessKey = yourAccessKeyWithReadOnly
	secretKey = yourPrivateKeyWithReadOnly
	ip = ipOfYourATWServer
	port = portOfYourATWServer

Screenshot
==========
![Image Alt](http://i68.tinypic.com/jpct9l.png)
![Image Alt](http://i65.tinypic.com/344rupw.png)
![Image Alt](http://i65.tinypic.com/sq1jqw.png)
![Image Alt](http://i64.tinypic.com/158045w.png)
![Image Alt](http://i65.tinypic.com/2lschaw.png)
![Image Alt](http://i65.tinypic.com/k9um1w.png)
![Image Alt](http://i64.tinypic.com/2uig4fc.png)

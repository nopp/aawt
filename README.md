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
    ==========
	Create an user atw with access_key and private_key
	Attach policy below on atw user:
	* AmazonEC2ReadOnlyAccess
	* IAMReadOnlyAccess
	* AmazonRDSReadOnlyAccess
	* CloudWatchReadOnlyAccess
	You need to enable "Monitor your estimated charges"
	* Billing & Cost Management > Preferences > Check "Receive Billing Alerts"

	Create a file /etc/atw/config.cfg with:
	=======================================

	[conf]
	regions = sa-east-1:Sao Paulo,us-east-1:Virginia # You need to use this "pattern"
	accessKey = yourAccessKeyWithReadOnly
	secretKey = yourPrivateKeyWithReadOnly
	ip = ipOfYourATWServer
	port = portOfYourATWServer


Screenshot
==========
![Image Alt](http://i65.tinypic.com/2ynmiz4.png)

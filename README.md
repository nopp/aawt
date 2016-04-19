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
	# git clone https://github.com/nopp/atw.git
	# cd atw
	-> configure the application
	# python atw.py

Configure
=========

	Create a file /etc/atw/config.cfg with:

	[conf]
	regions = sa-east-1:Sao Paulo,us-east-1:Virginia # You need to use this "pattern"
	accessKey = yourAccessKeyWithReadOnly
	secretKey = yourPrivateKeyWithReadOnly
	ip = ipOfYourATWServer
	port = portOfYourATWServer

Screenshot
==========
![Image Alt](http://i65.tinypic.com/2ynmiz4.png)

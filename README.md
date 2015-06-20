# ATW (AWS Tool Web)

Required
========
	Python + Flask

TODO
====
	* EC2 Search/List (done!)
	* S3 Search/List
	* RDS Search/List
	* AMI Search/List

Install
=======
	# yum install python-pip -y
	# pip install flask
	# pip install boto
	# git clone https://github.com/nopp/atw.git
	# cd atw
	-> configure the application
	# python atw.py

Configure
=========

	Create a file /etc/atw/config.cfg with:

	[conf]
	region = yourEC2region
	accessKey = yourAccessKeyWithEC2ReadOnly
	secretKey = yourPrivateKeyWithEC2ReadOnly
	ip = ipOfYourATWServer
	port = portOfYourATWServer

Screenshot
==========
![Image Alt](http://s16.postimg.org/o3fpy1rp1/Screen_Shot_2015_06_20_at_10.png)

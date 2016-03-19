# ATW (AWS Tool Web)

Required
========
	Python + Flask

TODO
====
	* EC2 Search/List (done!)
	* RDS Search/List (done!)

Install
=======
	# yum install python-pip -y
	# pip install flask
	# pip install boto
	# mkdir /var/log/atw/
	# git clone https://github.com/nopp/atw.git
	# cd atw
	-> configure the application
	# python atw.py

Configure
=========

	Create a file /etc/atw/config.cfg with:

	[conf]
	regions = sa-east-1:Sao Paulo,us-east-1:Virginia # You need to follow this "pattern"
	accessKey = yourAccessKeyWithEC2ReadOnly
	secretKey = yourPrivateKeyWithEC2ReadOnly
	ip = ipOfYourATWServer
	port = portOfYourATWServer

Screenshot
==========
![Image Alt](http://i63.tinypic.com/309li5j.png)

# ATW (AWS Tool Web)

Required
========
	Python + Flask

Install
=======
	yum install python-pip -y
	pip install flask
	pip install boto

Configure
=========

	Create a directory /etc/atw/ and file /etc/atw/config.cfg with:

	[conf]
	accessKey = yourAccessKeyWithEC2ReadOnly
	secretKey = yourPrivateKeyWithEC2ReadOnly

	Obs:. you need to change atw.py host and port to bind.

Start
=====
	python atw.py

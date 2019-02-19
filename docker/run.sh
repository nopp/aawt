#!/bin/bash
sed -i s/ipserver/0.0.0.0/ /etc/aawt/config.cfg
sed -i s/akey/"$akey"/ /etc/aawt/config.cfg
sed -i s/skey/"$skey"/ /etc/aawt/config.cfg

/usr/bin/python3 aawt.py

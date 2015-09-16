#!/bin/bash

apt-get update
apt-get -y install build-essential
apt-get -y install python-pip
apt-get -y install python-distribute
apt-get -y install python-tox
apt-get -y install python-dev
apt-get -y install libcurl4-openssl-dev
apt-get -y install libev4 libev-dev

apt-get -y install ntp ntpdate
service ntp start
ntpdate 0.pool.ntp.org

apt-get -y install nginx
rm -f /etc/nginx/conf.d/*
rm -f /etc/nginx/sites-enabled/*
cp sysconfig/nginx/the-best.conf /etc/nginx/conf.d/
service nginx restart

apt-get -y install supervisor
cp sysconfig/supervisor/the-best.conf /etc/supervisor/conf.d/

cp sysconfig/runservice.sh /opt

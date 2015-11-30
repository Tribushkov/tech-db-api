#! /usr/bin/env bash
# Variables
APPENV=local
DBHOST=localhost
DBNAME=db
DBUSER=root
DBPASSWD=root

echo -e "\n--- Installing now... ---\n"

echo -e "\n--- Updating packages list ---\n"
apt-get -qq update > /dev/null 2>&1

echo -e "\n--- Installing base packages ---\n"
apt-get -y install vim curl git httperf python-pip python-dev nginx> /dev/null 2>&1

echo -e "\n--- Installing python packages ---\n"
pip -q install flask mysql-python ujson gunicorn> /dev/null 2>&1

echo -e "\n--- Install MySQL specific packages and settings ---\n"
echo "mysql-server mysql-server/root_password password $DBPASSWD" | debconf-set-selections
echo "mysql-server mysql-server/root_password_again password $DBPASSWD" | debconf-set-selections
apt-get update > /dev/null 2>&1
apt-get -y install mysql-server python-mysqldb> /dev/null 2>&1

echo -e "\n--- Done! ---\n"
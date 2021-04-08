#!/usr/bin/env bash

if [[ $# -ne 4 ]];then
  echo "Usage script $0 <URL-Server> <IP-Router> <user> <password>"
  exit 1
fi

url=$1
ip=$2
usr=$3
pss=$4

curl ${url} -X PUT -d "ip=${ip}&user=${usr}&pwd=${pss}"
echo "Hecho"

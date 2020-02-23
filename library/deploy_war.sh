#!/bin/bash

source $1
curl -T $war_file -u $user:$pass 'http://'$server'/manager/text/deploy?path=/'$app_name'&update=true'

printf '{"changed": true, "failed": false, "msg": "Deployment complete"}'

echo Deploing time: $(date +"%T %D") \n Deploying user: $user >> /opt/tomcat/apache-tomcat-8.5.50/webapps/deploying_result.txt
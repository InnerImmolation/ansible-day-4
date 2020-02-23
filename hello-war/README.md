## Requirements
```
yum install -y maven git
git clone https://github.com/sbeliakou/hello-war.git
```

## Custom Data
Add following info into [build-info.txt](src/main/resources/build-info.txt):
```
Build time: 
Build Machine Name: 
Build User Name: 
```

## Building
```
mvn clean package -DbuildNumber=$BUILD_NUMBER
```

## Deploying

Copy buit war artifact into: /var/lib/tomcat/webapps/

Create file /var/lib/tomcat/webapps/deploy-info.txt with custom data:
```
Deployment time: 
Deploy User:
```

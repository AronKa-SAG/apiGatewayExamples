# Guide for SSL on API Gateway
## Create Truststore on Docker-Container
### 1. Get access to docker container:
> <code>docker exec -it name /bin/bash</code>

### 2. Create myTruststore.p12:
> <code>cd /opt/softwareag/jvm/jvm/bin</code>

> <code>keytool -genkey -alias client -keyalg RSA -keypass manage -storepass manage -keysize 2048 -keystore clientkeystore.p12 -storetype PKCS12</code>

> <code>keytool -export -keystore clientkeystore.p12 -alias client -file client.crt</code>

> <code>keytool -genkey -alias server -keyalg RSA -keypass manage -storepass manage -keysize 2048 -keystore myTruststore.p12 -storetype PKCS12</code>

> <code>keytool -import -keystore myTruststore.p12 -alias client -file client.crt</code>

### 3. Copy myTruststore.p12 to local machine:
> <code>docker ps</code>

Choose the right docker-container and copy the containerID.

> <code>docker cp *containerID*:/opt/softwareag/jvm/jvm/bin/*filename* *pathOnLocalMachine*</code>

## API Gateway: Settings
Go to API Gateway and log in via Administrator/manage.
Now go to the Administratorpage, open securitytab and click **Add truststore**. There you just need to give your truststore a name and import the **myTruststore.jks**-file. 

Next open the Ports-tab and click on Port 5543. There collapse the **Listener specific credentials** and selecdt myTruststore for truststore.

## POSTMAN
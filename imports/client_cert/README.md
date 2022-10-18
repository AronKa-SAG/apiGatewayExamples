# Guide for SSL on API Gateway
## Create Truststore on Docker-Container
### 1. Get access to docker container:
<code>docker exec -it *name* /bin/bash</code>

In my example the name is *apigateway-1011*.

### 2. Create myTruststore.p12:
<code>cd /opt/softwareag/jvm/jvm/bin</code>

Changes into the folder where the keytool is stored on the server.

<code>keytool -genkey -alias client -keyalg RSA -keypass manage -storepass manage -keysize 2048 -keystore clientkeystore.p12 -storetype PKCS12</code>

Generates a clientkeystore **clientkeystore.p12** with password **manage** .

<code>keytool -export -keystore clientkeystore.p12 -alias client -file client.crt</code>

Exports the certificate of **client** out of **clientkeystore.p12**.

<code>keytool -genkey -alias server -keyalg RSA -keypass manage -storepass manage -keysize 2048 -keystore myTruststore.p12 -storetype PKCS12</code>

Generates a truststore **myTruststore.p12** with the password **manage**.

<code>keytool -import -keystore myTruststore.p12 -alias client -file client.crt</code>

Imports the client-certificate into the truststore so that every call with the right certificate is trusted. 

### 3. Copy myTruststore.p12 to local machine:
<code>docker ps</code>

Choose the right docker-container and copy the containerID.

<code>docker cp *containerID*:/opt/softwareag/jvm/jvm/bin/*filename* *pathOnLocalMachine*</code>

### Alternatives:
#### 1) You can use **KeyStore Explorer** instead but it is recommended to understand the steps above.
#### 2) Use our run_docker_gw.py instead with the option client_cert.<br>
 <code>python run_docker_gw.py client_cert</code>

## API Gateway: Settings
Go to API Gateway and log in via Administrator/manage.
Now go to the administratorpage, open securitytab and click **Add truststore**. There you just need to give your truststore a name and import the **myTruststore.jks**-file. 

Next open the ports-tab and click on port 5543. There open the **Listener specific credentials** and select myTruststore for truststore. If not yet done: enable port 5543!

## POSTMAN
Go into **Settings>Certificates** and click on **Add Certificate**. The **Host** is *localhost:5543*. We already prepared the right .pfx-file so just click on select file and in **./imports/client_cert** select the file **client.pfx**. Now you should be ready to go!
# Docker-Gateway

- [Docker-Gateway](#docker-gateway)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Docker](#docker)
    - [Python](#python)
    - [npm](#npm)
    - [newman](#newman)
    - [Gateway / Devportal](#gateway--devportal)
  - [Usage](#usage)
    - [Setup](#setup)
    - [Testing](#testing)
      - [JWT, OpenID, OAuth2](#tests-for-authorization-incl-openid-oauth2-jwt)
    - [Accessing via localhost](#accessing-via-localhost)
  - [Introduction of Examples](#introduction-of-examples)
    - [What is keycloak?](#what-is-keycloak)
    - [OAuth2](#oauth2-included-in-example-keycloak)
    - [JWT](#jwt-included-in-example-keycloak)
    - [Client Certification](#client-certification-included-in-client_cert)

## Overview
This repository provides multiple example usecases for SAG webMethods API Gateway (in the following called **gateway**).
The repo uses the docker images from SAG, available on [Software AG's Docker Repo](https://containers.softwareag.com/products).

## Requirements
It is expected that [Docker](https://docs.docker.com/get-docker/), [Python](https://www.python.org/downloads/), [npm](https://nodejs.org/en/download/) and [newman (via npm)](https://www.npmjs.com/package/newman#getting-started) are installed on your system.

Docker images required:
- sagcr.azurecr.io/apigateway:10.11
- jboss/keycloak

## Installation
### Docker
First of all create a docker account and subscribe to [SAG API Gateway](https://hub.docker.com/publishers/softwareag). Then install Docker via Company Portal or download it [here](https://docs.docker.com/get-docker).

### Python
Install Python via Company Portal or download it [here](https://www.python.org/downloads/).
At setup check the box <b>install to PATH</b>. Elsewise you won't be able to call python via commandline.
If you forgot to check the box open **System Control>System & Security>Advanced System Settings>Environment variables** and edit the **Path**-entry under **Systemvariables**. Just add the installation-path of Python.

### npm
Install Node.js via Company Portal or download it [here](https://nodejs.org/en/download/). Make sure you leave everything at setup as default.

### newman
It is required that you have already installed npm. To check type <code>npm -v</code> in commandline.
Should you have installed npm, execute the command:
><code>npm install -g newman</code>

### Gateway / Devportal
To install gateway or devportal with docker, open the following link: [Software AG API Gateway](https://containers.softwareag.com/products/apigateway) or [Software AG Devportal](https://containers.softwareag.com/products/devportal).
On the website check the box <b>I agree to the Software AG's Terms and conditions</b> and click **Get the pull command**. Now store the token password somewhere save. Copy the command under **Docker login** and press **Got it!**.
To login to docker open a terminal and paste and execute the command. The command looks something like this:
><code>docker login *{Firstname}*-*{Lastname}*-sofwareag-com -p *{key}* sagcr.azurecr.io</code>

The last step is to copy the command under **Docker Pull Command** and paste and execute it in the terminal. This looks something like that:
><code>docker pull sagcr.azurecr.io/apigateway:*{versionnumber}*</code>

or

><code>docker pull sagcr.azurecr.io/devportal:*{versionnumber}*</code>

## Usage

### Setup
Make sure Docker Desktop is started.

Once it is started and you pulled the corresponding images, you can run the [run_docker_gw.py](run_docker_gw.py) file using the following syntax:<br>
><code>python run_docker_gw.py *{example_name}*</code>

If 'import requests' in pythonsript *run_docker_gw.py* doesn't work out execute the command <code>pip install requests</code>.

To view the list of all available examples, execute the command:
><code>python run_docker_gw.py lst</code>

### Testing
There is a test-unit-file called [testing.json](testing.json). Import this file in Postman.
#### Tests for authorization incl. OpenID, OAuth2, JWT
When you look at the tests carefully, you will notice that the tests do an API call <b>before</b> the actual API call. In that call it gets the token from keycloak. This token is then used in the actual API call to authenticate before gateway. Why is this even necessary? It is necessary because would you call keycloak directly the bearer-token attribute 'iss' would include 'localhost'. But because we are in a virtual network (to be more precised: docker-network) and the hostname of keycloak there is 'keycloak', gateway will refuse our request. When we call a gateway API, we are in the virtual network and then our bearer-token's attribute 'iss' will include 'keycloak' instead of 'localhost'. Look for yourself at [jwt.io](https://jwt.io/) and paste the bearer-tokens in there. To get a better understanding it is also useful to review the getKeycloakToken-API.

### Accessing via localhost
If you didn't change any configurations in the YML-files, you can access the products on the following ports:
| Product | Port |
| ------- | ---- |
| API GW 1 | 9072 |
| IS 1 - HTTP | 5555 |
| IS 1 - HTTPS | 5543 |
| API GW 2 | 19072 |
| IS 2 - HTTP | 15555 |
| Keycloak | 8080 |
| API Portal | 18101 |

## Introduction of Examples
In this chapter I will try to explain some of the more complex APIs to you.

But first I will explain keycloak by a little to you so that it is more understandable what some of the APIs are doing.
### What is keycloak?
Keycloak is an authentication-server. That means its purpose is to give certain permissions to certain persons. You for sure don't want an external to use your administrative APIs, right? So therefore you create so called 'clients' in keycloak. All of those clients have other permissions. For example the Administrator has access to all APIs, while an external only has access to one specific API. 
In API Gateway you also have the ability to give someone just read-permission. That means you are just able to make a GET-request. (further informations in [oauth2](#oauth2-included-in-example-keycloak))

### OAuth2 (included in example keycloak)
This API uses the method of OAuth2-authentication. It is seperated into two scopes. One scope is called 'WRITE'. With that scope your are just able to POST, PUT and DELETE data. The other is called 'READ' which only allows you to GET data. Internally those two API-scopes are linked to two seperate scopes in keycloak. And those two keycloak-scopes give the client x read-permission and the client y write-permission. That means: Should client x try to GET data, gateway will refuse the request and will instead give a response with statuscode 401 (unauthorized). But should client x try to PUT data, gateway will accept the request and puts the data.

### JWT (included in example keycloak)
TODO


### Client Certification (included in example client_cert)
You may have problems getting a valid response. This is caused by the fact that API Gateway refuses your request because you may have not deposit a certificate. Click [here](imports/client_cert/README.md) to solve this issue.

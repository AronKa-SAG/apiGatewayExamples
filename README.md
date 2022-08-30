# Docker-Gateway

- [Docker-Gateway](#docker-gateway)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Docker](#docker)
    - [Python](#python)
    - [npm](#npm)
    - [newman](#newman)
    - [Gateway](#gateway)
  - [Usage](#usage)
    - [Setup](#setup)
    - [Accessing via localhost](#accessing-via-localhost)

## Overview
This repository provides multiple example usecases for SAG webMethods API Gateway.
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
If you forgot to check the box open **System Control>System & Security>Advanced System Settings>Environment variables** and change the **Path**-entry under **Systemvariables**. Just add the installation-path of Python.

### npm
Install Node.js via Company Portal or download it [here](https://nodejs.org/en/download/). Make sure you leave everything at setup as default.

### newman
It is required that you have already installed npm. To check type <code>npm -v</code> in commandline.
Now install newman via commandline: <br>
><code>npm install -g newman</code>

### Gateway
To install gateway with docker open the following link: [Software AG API Gateways](https://containers.softwareag.com/products/apigateway).
On the website check the box <b>I agree to the Software AG's Terms and conditions</b> and click **Get the pull command**. Now store the token password somewhere save. Copy the command under **Docker login** and press **Got it!**.
To login to docker open a terminal and paste and execute the command. The command looks something like this:
><code>docker login *{Firstname}*-*{Lastname}*-sofwareag-com -p *{key}* sagcr.azurecr.io</code>

The last step is to copy the command under **Docker Pull Command** and paste and execute it in the terminal. This looks something like this:
><code>docker pull sagcr.azurecr.io/apigateway:*{versionnumber}*</code>

## Usage

### Setup
The repo can be used by running the [docker-compose file](docker-compose.yml) via commandline:
><code>docker-compose up -d</code>

This will create API Gateway and wS IS.

To run API Gateway execute the following on your terminal:
><code>docker run -d -p 5555:5555 -p 9072:9072 --hostname apigw-host --name apigw store/softwareag/apigateway-trial:*{versionnumber}*</code>

<b>&uarr; Modify this! &uarr;</b>

Should you have changed the YML-file just change the ports to the right ones.

Once Docker is started and you pulled the corresponding images, you can run the [run_docker_gw.py](run_docker_gw.py) file using the following syntax:<br>
><code>python run_docker_gw.py *{example_name}*</code>

If 'import requests' in pythonsript *run_docker_gw.py* doesn't work out execute the command <code>pip install requests</code>.

<br>The currently available *{example_name}* are given when entering a wrong *{example_name}*.

List of available examples:
- [empty] or *default* - imports all available examples
- *keycloak*
- *data_masking*
- *context_routing*
- *dynamic_routing*
- *websocket*
- *api_mashup*
- *client_cert*

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
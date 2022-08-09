# Docker-Gateway

- [Docker-Gateway](#docker-gateway)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Setup](#setup)
    - [Accessing via localhost](#accessing-via-localhost)


## Overview
This repository provides a way to create PoCs quickly for SAG webMethods API Gateway.
The repo uses the docker images from SAG, available on [Software AG's Docker Page](https://hub.docker.com/publishers/softwareag).
test

## Requirements
It is expected that [Docker](https://docs.docker.com/get-docker/), [Python](https://www.python.org/downloads/), [npm](https://nodejs.org/en/download/) and [newman (via npm)](https://www.npmjs.com/package/newman#getting-started) are installed on your system.

Docker images required:
- store/softwareag/apigateway-trial
- jboss/keycloak

## Usage

### Setup
The repo can be used by running the [docker-compose file](docker-compose.yml) via commandline:
<code>docker compose up -d</code>

Once Docker is started and you pulled the corresponding images, you can run the [run_docker_gw.py](run_docker_gw.py) file using the following syntax:
<code>python run_docker_gw.py *{poc_name}*</code>

The currently available *{poc_name}* are given when entering a wrong *{poc_name}*.

List of available PoCs:
- [empty] or *default* - imports all available PoCs
- *keycloak*
- *data_masking*
- *context_routing*
- *dynmic_routing*
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

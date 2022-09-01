from os import system
import os
import subprocess
import sys
import time
import requests
import json


# dict for PoC demos
poc_dict = {
    "default": "imports/full_GW-collection.json",
    "keycloak": "imports/keycloak-collection.json",
    "oauth": "imports/keycloak-collection.json",
    "external_as": "imports/keycloak-collection.json",
    "data_masking": "imports/data_masking-collection.json",
    "datamasking": "imports/data_masking-collection.json",
    "conditional_routing": "imports/conditional_routing-collection.json",
    "conditionalrouting": "imports/conditional_routing-collection.json",
    "dynamic_routing": "imports/dynamic_routing-collection.json",
    "dynamicrouting": "imports/dynamic_routing-collection.json",
    "websocket": "imports/websocket-collection.json",
    "ws": "imports/websocket-collection.json",
    "api_mashup": "imports/mashup-collection.json",
    "mashup": "imports/mashup-collection.json",
    "client_cert": "imports/client_cert-collection.json",
    "ssl": "imports/client_cert-collection.json",
    "certificate": "imports/client_cert-collection.json",
    "users": "imports/users-collection.json" # Gibt es nicht
}

# input args to choose demo
if len(sys.argv) > 2:
    raise KeyError("Too many arguments given via commandline!")
elif len(sys.argv) == 2:
    if sys.argv[1] in list(poc_dict.keys()):
        key = sys.argv[1]
    else:
        raise KeyError(f"As parameter use one of {list(poc_dict.keys())}")   
else:
    # get all files in imports folder for big demo
    key = "default"

healthy_gw = False
max_iterations = 10
iterations = 0
sleep_s = 20
health_check = "http://localhost:5555/rest/apigateway/health"

location = os.getenv('APPDATA')+'\\npm'
print(f"{location}, {key}")
if not os.path.exists(location):
    raise FileNotFoundError("newman was not installed! Please follow the install-instruction.")
    
# docker_location = 'C:/Users/y508854/OneDrive - Software AG/Documents/API Gateway Resources/Docker Gateway'
docker_run = 'docker compose up -d'
header = {
    "Accept": "application/json"
}

print("starting API GW via docker compose...")
return_code = subprocess.call(f"{docker_run}", shell=True)

while(iterations < max_iterations):
    try:
        r = requests.get(url = health_check, headers=header)
        if r.status_code == 200:
            print(f"API Gateway is up & running after {iterations + 1} iteration(s).")
            healthy_gw = True
            break
        else:
            print(f"API Gateway is running but healthcheck failed. Retry {iterations + 1} of {max_iterations}.")
            iterations += 1
            time.sleep(sleep_s)
    except requests.exceptions.ConnectionError:
        print(f"API Gateway is not up. Retry in 20s. Retry {iterations + 1} of {max_iterations}.")
        iterations += 1
        time.sleep(sleep_s)
    
if healthy_gw:
    print(f"Starting API GW imports using {key} collection")
    if not os.path.exists(os.getenv('TEMP')+"/conf_apigw.log"):
        subprocess.call(f"{location}/newman run conf.json", shell=True)
        with open(os.getenv('TEMP')+"/conf_apigw.log", 'w') as f:
            f.write(f"Configuration on {time.asctime(time.localtime(time.time()))} was successful!")
    subprocess.call(f"{location}\\newman.cmd run {poc_dict.get(key)}", shell=True)
else:
    raise ConnectionError(f"Couldn't connect to API Gateway in {max_iterations} tries. Terminating...")

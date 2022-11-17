import os
import subprocess
import sys
import time
try:
    import requests
except:
    # installs package requests if not installes
    subprocess.call("pip install requests", shell=True)
    import requests

# This function will return name
# i.e. : nameOf("collection-example.json") -> "example"
def nameOf(file : str) -> str:
    name : str = ""
    partOfName : bool = False
    for c in file:
        if c == ".":
            partOfName = False
        if partOfName:
            name += c
        if c == "-":
            partOfName = True
    return name

# available import-options (apis) for apigateway
poc_dict = {}

# dict for PoC demos
for file in os.listdir("./imports"):

    # checks if file includes "collection" in it's name and checks if it is a json-file
    if "collection" in file and file.endswith('.json'):
        poc_dict[nameOf(file)] = f"./imports/{file}"

# input args to choose demo
options : list = list(poc_dict.keys())

if len(sys.argv) > 2:
    raise KeyError("Too many arguments given via commandline!")
elif len(sys.argv) == 2:
    if sys.argv[1] in options:
        key = sys.argv[1]
    else:
        # will print all options if no valid option was given as additional call-parameter
        # and asks for valid input
        key = 0
        for i in options:
            print(f"-\t{i}")
        print("-\tfull")
        while not (key  in options or key == "full"):
            key = input("Insert one of the options above:\n> ")
else:
    # when no additional call-parameter is given, full demo will be selected for import
    key = "full"

base = "http://localhost:5555/rest/apigateway"
health_check = f"{base}/health"
loadbalancer = f"{base}/configurations/loadBalancer"
auth = ("Administrator","manage")
healthy_gw = False
max_iterations = 12
iterations = 0
sleep_s = 20
elasticsearch = 'docker run -d -e "discovery.type=single-node" -e "xpack.security.enabled=false" -u elasticsearch --network api-gateway-network --name elasticsearch --hostname elastic -p 9200:9200 --net-alias elastic docker.elastic.co/elasticsearch/elasticsearch:8.2.3'
devportal = 'docker run -d -e SPRING_ELASTICSEARCH_REST_URIS="http://elastic:9200" --network api-gateway-network --name devportal --hostname devportal -p 80:8083 sagcr.azurecr.io/devportal:10.15'
statuscall_addr = "http://localhost:9200/_status"
healthy_es = False


# checks if npm exists
location = os.getenv('APPDATA')+'\\npm'
if not os.path.exists(location):
    raise FileNotFoundError("newman was not installed! Please read README.md carefully!")

docker_run = 'docker compose up -d'

header_es = {
    "Accept": "appliaction/json"
}

header_gw = {
    "Accept": "application/json",
    "Authorization": "Basic QWRtaW5pc3RyYXRvcjptYW5hZ2U="
}


# will check if wsl is needed and if so if .wslconfig exists
# will create .wslconfig if it doesn_t exist
wsl_config_path = os.getenv('USERPROFILE')+"\.wslconfig"
if (subprocess.call(f"wsl --status", shell=True) ==  0) and not(os.path.exists(wsl_config_path)):
    with open(wsl_config_path, "w") as f:
        wsl_settings = "[wsl2]\nmemory = 8GB\nkernelCommandLine = sysctl.vm.max_map_count = 262144 && ulimit -n 65536"
        f.write(wsl_settings)
        # main = "wsl -d docker-desktop"
        # subprocess.call(f"{main} ulimit -n 65536",shell=True)
        # subprocess.call(f"{main} sysctl -w fs.file-max=200000",shell=True)
        # subprocess.call(f"{main} sysctl -w vm.max_map_count=",shell=True)

x = input("Do you want to compose API Gateway? (by default 'n') [y/n]\n> ").lower()
if x in {"y", "yes", "j"}:
    print("starting API GW via docker compose...")
    return_code = subprocess.call(f"{docker_run}", shell=True)

    # start elasticsearch
    subprocess.call(f"{elasticsearch}", shell=True)

    # Will exit when {max_iterations} is reached 
    while(iterations < max_iterations):
        try:
            # calls elasticsearch to check health
            r = requests.get(url = statuscall_addr, headers = header_es)

            if r.status_code == 200:
                # will run devportal if http-call was successful
                print("Elasticsearch is up and running! Initializing devportal...")
                healthy_es = False
                subprocess.call(f"{devportal}", shell=True)
            else:
                # waits {sleep_s} seconds till next http-call
                print(f"Healthcheck failed! Retry in {sleep_s}s. [{iterations + 1}/{max_iterations}]")
                iterations += 1
                time.sleep(sleep_s)
        except:
            # waits {sleep_s} seconds till next http-call
            print(f"Waiting for elasticsearch... [{iterations + 1}/{max_iterations}]")
            iterations += 1
            time.sleep(sleep_s)

    # will raise error when elasticsearch couldn't start in {max_iterations * sleep_s} seconds
    if(not(healthy_es)):
        raise ConnectionError("Could not start elasticsearch and therefore was not able to install devportal!")

iterations = 0

# will exit when {max_iterations} is reached
while(iterations < max_iterations):
    try:
        # calls apigateway to check health
        r = requests.get(url = health_check, headers = header_gw)

        if r.status_code == 200:
            # will break if http-call was successful
            print(f"API Gateway is up & running after {iterations + 1} iteration(s).")
            healthy_gw = True
            break
        else:
            # waits {sleep_s} seconds till next http-call
            print(f"API Gateway is running but healthcheck failed. Retry {iterations + 1} of {max_iterations}.")
            iterations += 1
            time.sleep(sleep_s)
    except requests.exceptions.ConnectionError:
        # waits {sleep_s} seconds till next http-call
        print(f"API Gateway is not up. Retry in 20s. Retry {iterations + 1} of {max_iterations}.")
        iterations += 1
        time.sleep(sleep_s)
    
if healthy_gw:
    print(f"Starting API GW imports using {key} collection")
    
    # grabs loadbalancersettings of apigateway
    r = requests.get(url = loadbalancer, headers = header_gw)
    
    # checks if httpUrls is set. If not a config-file will be pushed to apigateway 
    if int(len(r.json()["httpUrls"])) == 0:
        subprocess.call(f"{location}/newman run conf.json", shell=True)

    # will import all collections
    if key == "full":
        for i in list(poc_dict.keys()):
            subprocess.call(f"{location}/newman run {poc_dict.get(i)}", shell=True)
    else:
        # will import {key} collection
        subprocess.call(f"{location}/newman run {poc_dict.get(key)}", shell=True)
else:
    # raises error when apigateway couldn_t start
    raise ConnectionError(f"Couldn't connect to API Gateway in {max_iterations} tries. Terminating...")

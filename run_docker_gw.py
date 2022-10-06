from os import system
import os
import subprocess
import sys
import time
import requests
import base64

def nameOf(file):
    name = ""
    partOfName = False
    for c in file:
        if c == ".":
            partOfName = False
        if partOfName:
            name += c
        if c == "-":
            partOfName = True
    return name


poc_dict = {}

# dict for PoC demos
for file in os.listdir("./imports"):
    if "collection" in file:
        poc_dict[nameOf(file)] = f"./imports/{file}"

# input args to choose demo
options = list(poc_dict.keys())

if len(sys.argv) > 2:
    raise KeyError("Too many arguments given via commandline!")
elif len(sys.argv) == 2:
    if sys.argv[1] in options:
        key = sys.argv[1]
    else:
        key = 0
        for i in options:
            print(f"-\t{i}")
        print("-\tfull")
        while key not in options and key != "full":
            key = input("Insert one of the options above:\n> ")
            if key == "exit":
                exit()
else:
    # get all files in imports folder for big demo
    key = "full"

base = "http://localhost:5555/rest/apigateway"
health_check = f"{base}/health"
loadbalancer = f"{base}/configurations/loadBalancer"
auth =("Administrator",base64.b64decode("bWFuYWdl").decode("utf-8"))
healthy_gw = False
max_iterations = 10
iterations = 0
sleep_s = 20

location = os.getenv('APPDATA')+'\\npm'
if not os.path.exists(location):
    raise FileNotFoundError("newman was not installed! Please follow the install-instruction.")
    
# docker_location = 'C:/Users/y508854/OneDrive - Software AG/Documents/API Gateway Resources/Docker Gateway'
docker_run = 'docker compose up -d'
header = {
    "Accept": "application/json"
}

x = input("Do you want to compose API Gateway? (by default 'n') [y/n]\n> ").lower()
if x=="y" or x=="yes" or x=="j":
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
    
    r = requests.get(url = loadbalancer, headers = header, auth = auth)
    if int(len(r.json()["httpUrls"])) == 0:
        subprocess.call(f"{location}/newman run conf.json", shell=True)
    if key == "full":
        for i in list(poc_dict.keys()):
            subprocess.call(f"{location}/newman run {poc_dict.get(i)}", shell=True)
    else:
        subprocess.call(f"{location}/newman run {poc_dict.get(key)}", shell=True)
else:
    raise ConnectionError(f"Couldn't connect to API Gateway in {max_iterations} tries. Terminating...")

import os
import subprocess
import sys
import time
try:
    import requests
except:
    # installs package requests if not installed
    subprocess.call("pip install requests", shell=True)
    import requests


max_iterations = 12
sleep_s = 20
create_network = "docker network create devportal-network"
elasticsearch = 'docker run -d -e "discovery.type=single-node" -e "xpack.security.enabled=false" -u elasticsearch --net devportal-network --name elasticsearch --hostname elasticsearch -p 9200:9200 --net-alias elasticsearch docker.elastic.co/elasticsearch/elasticsearch:8.2.3'
devportal = 'docker run -d -e SPRING_ELASTICSEARCH_REST_URIS="http://elasticsearch:9200" --net devportal-network --name devportal --hostname devportal -p 80:8083 sagcr.azurecr.io/devportal:10.15'
statuscall_addr = "http://localhost:9200/_status"
healthy_es = False

header_es = {
    "Accept": "appliaction/json"
}

wsl_config_path = os.getenv('USERPROFILE')+"\.wslconfig"
if (subprocess.call(f"wsl --status", shell=True) ==  0) and not(os.path.exists(wsl_config_path)):
    with open(wsl_config_path, "w") as f:
        wsl_settings = "[wsl2]\nmemory = 8GB\nkernelCommandLine = sysctl.vm.max_map_count=262144 && sysctl.fs.file-max=200000 && ulimit -n 65536"
        f.write(wsl_settings)

x = input("Do you want to compose API Gateway? (by default 'n') [y/n]\n> ").lower()
if x in {"y", "yes", "j"}:
    # create docker-network
    subprocess.call(f"{create_network}", shell=True)

    # start elasticsearch
    subprocess.call(f"{elasticsearch}", shell=True)
    print("Starting elasticsearch...")

    # Will exit when {max_iterations} is reached 
    for iterations in range(max_iterations):
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

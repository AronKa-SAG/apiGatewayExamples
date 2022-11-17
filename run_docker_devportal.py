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


max_iterations = 12
iterations = 0
sleep_s = 20
elasticsearch = 'docker run -d -e "discovery.type=single-node" -e "xpack.security.enabled=false" -u elasticsearch --network api-gateway-network --name elastic --hostname elastic -p 9200:9200 --net-alias elastic docker.elastic.co/elasticsearch/elasticsearch:8.2.3'
devportal = 'docker run -d -e SPRING_ELASTICSEARCH_REST_URIS="http://elastic:9200" --network api-gateway-network --name devportal --hostname devportal -p 80:8083 sagcr.azurecr.io/devportal:10.15'
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
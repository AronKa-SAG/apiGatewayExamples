import sys
import requests

base = "http://localhost:5555/rest/apigateway"
user = "Administrator"
pwd = "manage"
headers = {
    "Accept":"application/json"
}
session = requests.session()
session.auth = (user,pwd)
session.headers.update(headers)

apiIDs = []

def doWork(method):
    if method == "delete":
        doWork("deactivate")
        for api in response["apiResponse"]:
            session.delete(f"{base}/apis/{api['api']['id']}?forceDelete=true")
        return
    elif method == "deactivate":
        state = True
        do = "deactivate"
    else:
        state = False
        do = "activate"

    for api in response["apiResponse"]:
        if api["api"]["isActive"] == state:
            apiIDs.append(api["api"]["id"])

    while len(apiIDs)!=0:
        session.put(f"{base}/apis/{apiIDs.pop()}/{do}")


response = session.get(f"{base}/apis").json()

x = 0
commands = {
#   option  :[function to call, description]
    "-a"    :["activate","Activate all APIs"],
    "-d"    :["deactivate","Deactivate all APIs"],
    "-rm"   :["delete","Deactivate and remove all APIs"]
}

while(x not in commands):
    if len(sys.argv) < 2:
        print("Type one of the following commands:")
        for x in commands:
            print(f"{x}\t: {commands[x][1]}")
        x = input("\n> ")
    else:  
        x = sys.argv[1]
        if len(sys.argv) > 2:
            x += f" {sys.argv[2]}"
    if x in list(commands.keys()):
        doWork(commands[x][0])
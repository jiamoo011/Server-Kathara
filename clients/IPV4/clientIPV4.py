import requests

url = "http://127.0.0.1:5000"

lab_name = "lab1"

machines = ["pc1","pc2","pc3","r1","r2"]

interfaces_config = [
    {"machine": "pc1", "domain": "A"},
    {"machine": "r1", "domain": "A"},
    {"machine": "r1", "domain": "B"},
    {"machine": "pc2", "domain": "C"},
    {"machine": "pc3", "domain": "C"},
    {"machine": "r2", "domain": "C"},
    {"machine": "r2", "domain": "B"}
]

startup_configs = [
    {
        "machine_name": "pc1",
        "commands": [
            "ip address add 195.11.14.5/24 dev eth0",
            "ip link set dev eth0 up",
            "ip route add default via 195.11.14.1"
        ]
    },

    {
        "machine_name": "pc2",
        "commands": [
            "ip address add 200.1.1.7/24 dev eth0",
            "ip link set dev eth0 up",
            "ip route add default via 200.1.1.1"
        ]
    },

    {
        "machine_name": "pc3",
        "commands": [
            "ip address add 200.1.1.3/24 dev eth0",
            "ip link set dev eth0 up",
            "ip route add default via 200.1.1.1"
        ]
    },

    {
        "machine_name": "r1",
        "commands": [
            "ip address add 195.11.14.1/24 dev eth0",
            "ip link set dev eth0 up",
            "ip address add 100.0.0.9/30 dev eth1",
            "ip link set dev eth1 up",
            "ip route add 200.1.1.0/24 via 100.0.0.10 dev eth1"
        ]
    },
    
    {
        "machine_name": "r2",
        "commands": [
            "ip address add 200.1.1.1/24 dev eth0",
            "ip link set dev eth0 up",
            "ip address add 100.0.0.10/30 dev eth1",
            "ip link set dev eth1 up",
            "ip route add 195.11.14.0/24 via 100.0.0.9 dev eth1"
        ]
    }
]

print("Creating lab:")
url_create_lab = f"{url}/lab/create"
payload_lab = {"lab_name": lab_name}

try: 
    requests.post(url_create_lab, json=payload_lab)
    
except Exception as e: print(f"Error: {e}")

url_create_machine= f"{url}/lab/machine"

for machine_name in machines:
    params = {"lab_name":lab_name}
    body = {"name" :machine_name, "meta": {"ipv6":False}}

    response1 = requests.post(url_create_machine,params=params, json=body)
    if (response1.status_code == 200): print(response1.json())
    else: print(str(response1.status_code), response1.json())

url_interface= f"{url}/lab/machine/interface"

for iface in interfaces_config:
    params={"lab_name": lab_name, "machine_name": iface["machine"], "domain": iface["domain"]}
    response2 = requests.post(url_interface, params = params)

    if (response2.status_code == 200): print(response2.json())
    else: print(str(response2.status_code), response2.json())


for config in startup_configs:
    resp = requests.post(f"{url}/lab/machine/startup", params={"lab_name": lab_name}, json=config)
    if (resp.status_code == 200): print(resp.json())
    else: print(str(resp.status_code), resp.json())

url_deploy = f"{url}/lab/deploy"
params = {"lab_name": lab_name}
print(f"Trying to deploy {lab_name}...")
response4 = requests.post(url_deploy, params = params)

if(response4.status_code==200): print(response4.json())

else: print(f"{lab_name} deployment failed")
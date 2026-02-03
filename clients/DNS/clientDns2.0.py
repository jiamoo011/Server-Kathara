import requests

lab_name = "labDNS"

url = "http://127.0.0.1:5000"

machines = ["pc1", "pc2" , "dnsit", "localuni", "dnsnet", "dnsroot", "dnsstart", "localstart", "dnsuni"]

interfaces_config = [
    {"machine": "pc1", "domain": "A"},
    {"machine": "pc2", "domain": "A"},
    {"machine": "dnsit", "domain": "A"},
    {"machine": "dnsnet", "domain": "A"},
    {"machine": "dnsroot", "domain": "A"},
    {"machine": "dnsstart", "domain": "A"},
    {"machine": "localstart", "domain": "A"},
    {"machine": "localuni", "domain": "A"},
    {"machine": "dnsuni", "domain": "A"}
]

startup_configs = [
    {
        "machine_name": "pc1",
        "commands":[
            """ip address add 192.168.0.111/24 dev eth0"""
        ]
    },
        {
        "machine_name": "pc2",
        "commands":[
            """ip address add 192.168.0.222/24 dev eth0"""
        ]
    },
        {
        "machine_name": "dnsit",
        "commands":[
            """ip address add 192.168.0.1/24 dev eth0
systemctl start bind9"""
        ]
    },
        {
        "machine_name": "dnsnet",
        "commands":[
            """ip address add 192.168.0.2/24 dev eth0
systemctl start bind9"""
        ]
    },
        {
        "machine_name": "dnsroot",
        "commands":[
            """ip address add 192.168.0.5/24 dev eth0
systemctl start bind9"""
        ]
    },
        {
        "machine_name": "dnsstart",
        "commands":[
            """ip address add 192.168.0.22/24 dev eth0
systemctl start bind9"""
        ]
    },
        {
        "machine_name": "localstart",
        "commands":["""ip address add 192.168.0.220/24 dev eth0
systemctl start bind9"""

        ]
    },
        {
        "machine_name": "localuni",
        "commands":[
            """ip address add 192.168.0.110/24 dev eth0
systemctl start bind9"""
        ]
    },
        {
        "machine_name": "dnsuni",
        "commands":[
            """ip address add 192.168.0.11/24 dev eth0
            systemctl start bind9"""      
        ]
    }
]


resolver_configs = [
    {
        "machine_name": "pc1",
        "files": [
            {
                "src": "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/pc1/etc/resolv.conf",
                "path": "/etc/resolv.conf"
            }
        ]
    },
    {
        "machine_name": "pc2",
        "files" : [
            {
                "src": "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/pc2/etc/resolv.conf",
                "path": "/etc/resolv.conf"
            }
        ]
    }
]

dns_config = [
    {
        "machine_name" : "dnsit",
        "files": [
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsit/etc/bind/db.it",
                "path" : "/etc/bind/db.it"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsit/etc/bind/db.root",
                "path": "/etc/bind/db.root"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsit/etc/bind/named.conf",
                "path" : "/etc/bind/named.conf"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsit/etc/bind/named.conf.options",
                "path": "/etc/bind/named.conf.options"
            }         
        ]
    },
    {
        "machine_name": "dnsnet",
        "files":[
            {
                "src": "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsnet/etc/bind/db.net",
                "path": "/etc/bind/db.net"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsnet/etc/bind/db.root",
                "path": "/etc/bind/db.root"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsnet/etc/bind/named.conf",
                "path": "/etc/bind/named.conf"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsnet/etc/bind/named.conf.options",
                "path" : "/etc/bind/named.conf.options"
            }
        ]
    },
    {
        "machine_name":"dnsroot",
        "files": [
            {
                "src": "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsroot/etc/bind/db.root",
                "path": "/etc/bind/db.root"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsroot/etc/bind/named.conf",
                "path" : "/etc/bind/named.conf"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsroot/etc/bind/named.conf.options",
                "path" : "/etc/bind/named.conf.options"
            }
        ]
    },
    {
        "machine_name": "dnsstart",
        "files":[
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsstart/etc/bind/db.net.startup",
                "path": "/etc/bind/db.net.startup" 
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsstart/etc/bind/db.root",
                "path" : "/etc/bind/db.root"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsstart/etc/bind/named.conf",
                "path" : "/etc/bind/named.conf"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsstart/etc/bind/named.conf.options",
                "path" : "/etc/bind/named.conf.options"
            }
        ]
    },
    {
        "machine_name" :"dnsuni",
        "files":[
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsuni/etc/bind/db.it.uniroma3",
                "path" : "/etc/bind/db.it.uniroma3"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsuni/etc/bind/db.root",
                "path" : "/etc/bind/db.root"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsuni/etc/bind/named.conf",
                "path" : "/etc/bind/named.conf"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/dnsuni/etc/bind/named.conf.options",
                "path": "/etc/bind/named.conf.options"
            }
        ]
    },
    {
        "machine_name" : "localstart",
        "files" : [
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/localstart/etc/bind/db.root",
                "path" : "/etc/bind/db.root"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/localstart/etc/bind/named.conf",
                "path": "/etc/bind/named.conf"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/localstart/etc/bind/named.conf.options",
                "path" : "/etc/bind/named.conf.options"
            }
        ]
    },
    {
        "machine_name" : "localuni",
        "files":[
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/localuni/etc/bind/db.root",
                "path" : "/etc/bind/db.root"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/localuni/etc/bind/named.conf",
                "path" : "/etc/bind/named.conf"
            },
            {
                "src" : "C:/Users/giamm/Documents/Università/Tirocinio/srcDNS/localuni/etc/bind/named.conf.options",
                "path" : "/etc/bind/named.conf.options"
            }
        ]
    },
]

print (f"Creating {lab_name}...")

url_create_lab = f"{url}/lab/create"
payload_lab = {"lab_name": lab_name}

try: requests.post(url_create_lab, json=payload_lab)
    
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

    if (response2.status_code == 200): print("Interface configurated!", response2.json())
    else: print(str(response2.status_code), response2.json())

for config in startup_configs:
    resp = requests.post(f"{url}/lab/machine/startup", params={"lab_name": lab_name}, json=config)
    if (resp.status_code == 200): print(resp.json())
    else: print(str(resp.status_code), resp.json())

for resolver in resolver_configs:
    resp = requests.post(f"{url}/lab/machine/file/path", params={"lab_name": lab_name}, json=resolver)
    if (resp.status_code == 200): print(resp.json())
    else: print (str(resp.status_code), resp.json())

for dns in dns_config:
    responseDns = requests.post(f"{url}/lab/machine/file/path", params={"lab_name":lab_name}, json = dns)
    if (responseDns.status_code == 200): print(responseDns.json())
    else: print (str(responseDns.status_code), responseDns.json())                    

url_deploy = f"{url}/lab/deploy"
params = {"lab_name": lab_name}

print(f"Trying to deploy {lab_name}...")

response4 = requests.post(url_deploy, params = params)

if(response4.status_code==200): print(response4.json())

else: print(f"{lab_name} deployment failed")
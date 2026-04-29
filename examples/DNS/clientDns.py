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
        "commands":[
            """ip address add 192.168.0.220/24 dev eth0
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
        "machine_name":"pc1",
        "files":[
           {
               "path":"/etc/resolv.conf",
               "content":"""nameserver 192.168.0.110
search uniroma3.it
options single-request"""
           }
        ]
    },
    {
        "machine_name" :"pc2",
        "files":[
            {
                "path":"/etc/resolv.conf",
                "content":"""nameserver 192.168.0.220
search startup.net
options single-request"""
            }
        ]
    }
]

dns_configs = [
    {
        "machine_name": "dnsit",
        "files": [
            {
                "path": "/etc/bind/db.it",
                "content": """$TTL 60000
@       IN      SOA     dnsit.it.    root.dnsit.it. (
                        2024120401 ; serial
                        28800 ; refresh
                        14400 ; retry
                        3600000 ; expire
                        0 ; negative cache ttl
                        )
@               IN      NS      dnsit.it.
dnsit.it.       IN      A       192.168.0.1
uniroma3.it.    IN      NS      dnsuni.uniroma3.it.
dnsuni.uniroma3.it. IN  A       192.168.0.11"""
            },
            {
                "path": "/etc/bind/db.root",
                "content": 
                """.                   IN  NS    ROOT-SERVER.
ROOT-SERVER.        IN  A     192.168.0.5"""
            },
            {
                "path":"/etc/bind/named.conf",
                "content": """include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};

zone "it" {
    type master;
    file "/etc/bind/db.it";
};"""
            },
            {
                "path": "/etc/bind/named.conf.options",
                "content": """options { directory "/var/cache/bind"; };"""
            }
        ]
    },
    {
        "machine_name": "dnsnet",
        "files":[
            {
                "path": "/etc/bind/db.net",
                "content": """$TTL 60000
@               IN      SOA     dnsnet.net.    root.dnsnet.net. (
                        2024120401 ; serial
                        28800 ; refresh
                        14400 ; retry
                        3600000 ; expire
                        0 ; negative cache ttl
                        )
@                    IN      NS      dnsnet.net.
dnsnet.net.          IN      A       192.168.0.2

startup.net.          IN     NS      dnsstart.startup.net.
dnsstart.startup.net. IN     A       192.168.0.22"""
            },
            {
                "path": "/etc/bind/db.root",
                "content": """
.                   IN  NS    ROOT-SERVER.
ROOT-SERVER.        IN  A     192.168.0.5"""
            },
            {
                "path": "/etc/bind/named.conf",
                "content": """include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};

zone "net" {
    type master;
    file "/etc/bind/db.net";
};"""
            },
            {
                "path" : "/etc/bind/named.conf.options",
                "content": """options { directory "/var/cache/bind"; };"""
            }
        ]
    },
    {
        "machine_name": "dnsroot",
        "files": [
            {
                "path" : "/etc/bind/db.root",
                "content": """$TTL 60000
@               IN      SOA     ROOT-SERVER.    root.ROOT-SERVER. (
                        2024120401 ; serial
                        28800 ; refresh
                        14400 ; retry
                        3600000 ; expire
                        0 ; negative cache ttl
                        )

@               IN      NS      ROOT-SERVER.
ROOT-SERVER.	IN	A	192.168.0.5

it.		        IN 	NS	dnsit.it.
dnsit.it.	    IN 	A	192.168.0.1

net.		    IN	NS	dnsnet.net.
dnsnet.net.	    IN	A	192.168.0.2"""
            },
            {
                "path": "/etc/bind/named.conf",
                "content": """include "/etc/bind/named.conf.options";

zone "." {
    type master;
    file "/etc/bind/db.root";
};"""
            },
            {
                "path": "/etc/bind/named.conf.options",
                "content" : """options { directory "/var/cache/bind"; };"""
            }
        ]
    },
    {
        "machine_name": "dnsstart",
        "files":[
            {
                "path": "/etc/bind/db.net.startup",
                "content" : """$TTL 60000
@               IN      SOA     dnsstart.startup.net.    root.dnsstart.startup.net. (
                        2024120401 ; serial
                        28 ; refresh
                        14400 ; retry
                        3600000 ; expire
                        15 ; negative cache ttl
                        )
@                          IN      	NS      	dnsstart.startup.net.
dnsstart.startup.net.      IN      	A       	192.168.0.22
pc2.startup.net.		   IN		A		192.168.0.222
localstart.startup.net.	   IN		A		192.168.0.220"""
            },
            {
                "path": "/etc/bind/db.root",
                "content" : """
.                   IN  NS    ROOT-SERVER.
ROOT-SERVER.        IN  A     192.168.0.5"""
            },
            {
                "path": "/etc/bind/named.conf",
                "content": """include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};

zone "startup.net" {
    type master;
    file "/etc/bind/db.net.startup";
};"""
            },
            {
                "path": "/etc/bind/named.conf.options",
                "content" : """options { directory "/var/cache/bind"; };"""
            }
        ]
    },
    {
        "machine_name": "dnsuni",
        "files":[
            {
                "path" : "/etc/bind/db.it.uniroma3",
                "content": """$TTL 60000
@               IN      SOA     dnsuni.uniroma3.it.    root.dnsuni.uniroma3.it. (
                        2024120401 ; serial
                        28 ; refresh
                        14 ; retry
                        3600000 ; expire
                        0 ; negative cache ttl
                        )

@						IN	NS	dnsuni.uniroma3.it.
dnsuni.uniroma3.it.		IN	A	192.168.0.11

pc1.uniroma3.it.		IN	A	192.168.0.111
localuni.uniroma3.it.	IN	A	192.168.0.110"""
            },
            {
                "path": "/etc/bind/db.root",
                "content": """
.                   IN  NS    ROOT-SERVER.
ROOT-SERVER.        IN  A     192.168.0.5"""
            },
            {
                "path" : "/etc/bind/named.conf",
                "content" :"""include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};

zone "uniroma3.it" {
    type master;
    file "/etc/bind/db.it.uniroma3";
};"""
            },
            {
                "path":"/etc/bind/named.conf.options",
                "content":"""options { directory "/var/cache/bind"; };"""
            }
        ]
    },
    {
        "machine_name" : "localstart",
        "files" : [
            {
                "path": "/etc/bind/db.root",
                "content": """
.                   IN  NS    ROOT-SERVER.
ROOT-SERVER.        IN  A     192.168.0.5"""
            },
            {
                "path" :"/etc/bind/named.conf",
                "content" : """include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};"""
            },
            {
                "path":"/etc/bind/named.conf.options",
                "content" :"""options {
directory "/var/cache/bind";
allow-recursion { 192.168.0.0/24; };
recursion yes;
dnssec-validation no;
};"""#filter-aaaa-on-v4 yes;
            }
        ]
    },
    {
        "machine_name": "localuni",
        "files": [
            {
                "path" :"/etc/bind/db.root",
                "content": """
.                   IN  NS    ROOT-SERVER.
ROOT-SERVER.        IN  A     192.168.0.5"""
            },
            {
                "path":"/etc/bind/named.conf",
                "content" : """include "/etc/bind/named.conf.options";

zone "." {
    type hint;
    file "/etc/bind/db.root";
};"""
            },
            {
                "path":"/etc/bind/named.conf.options",
                "content":"""options {
directory "/var/cache/bind";
allow-recursion { 192.168.0.0/24; };
recursion yes;
dnssec-validation no;
};"""#filter-aaaa-on-v4 yes;
            }
        ]
    }
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
    resp = requests.post(f"{url}/lab/machine/file/string", params={"lab_name": lab_name}, json = resolver)
    if (resp.status_code == 200): print(resp.json())
    else: print (str(resp.status_code), resp.json())

for dns in dns_configs:
    responseDns = requests.post(f"{url}/lab/machine/file/string", params={"lab_name":lab_name}, json = dns)
    if (responseDns.status_code == 200): print(responseDns.json())
    else: print (str(responseDns.status_code), responseDns.json())                    

url_deploy = f"{url}/lab/deploy"
params = {"lab_name": lab_name}

print(f"Trying to deploy {lab_name}...")
response4 = requests.post(url_deploy, params = params)

if(response4.status_code==200): print(response4.json())

else: print(f"{lab_name} deployment failed")
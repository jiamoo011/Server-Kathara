import requests, time

URL_SERVER = "http://127.0.0.1:5000"

machines = ["router", "dnsroot","dnsit", "dnsnet", "dnsstart", "dnsuni", "localuni", "localstart", "pc1", "pc2"]

interfaces = [
    {"machine": "router", "domain": "A"},
    {"machine": "router", "domain": "B"},
    {"machine": "router", "domain": "C"},
    {"machine": "dnsroot", "domain": "A"},
    {"machine": "dnsit", "domain": "A"},
    {"machine": "dnsnet", "domain": "A"},
    {"machine": "dnsuni", "domain": "B"},
    {"machine": "localuni", "domain": "B"},
    {"machine": "dnsstart", "domain" : "C"},
    {"machine": "localstart", "domain": "C"},
    {"machine": "pc1", "domain": "B"},
    {"machine": "pc2", "domain": "C"}
]

startup =  [
    {
        "machine_name": "router",
        "commands":[
            "ip address add 192.168.0.254/24 dev eth0",
            "ip -6 address add fd00:0::254/64 dev eth0",
            "ip address add 192.168.1.254/24 dev eth1",
            "ip -6 address add fd00:1::254/64 dev eth1",
            "ip address add 192.168.2.254/24 dev eth2",
            "ip -6 address add fd00:2::254/64 dev eth2",
            "sysctl -w net.ipv4.ip_forward=1",
            "sysctl -w net.ipv6.conf.all.forwarding=1"
        ]
    },
    {
        "machine_name": "pc1",
        "commands":[
            "ip address add 192.168.1.111/24 dev eth0",
            "ip -6 address add fd00:1::111/64 dev eth0",
            "ip route add default via 192.168.1.254",
            "ip -6 route add default via fd00:1::254"
        ]
    },
    {
        "machine_name": "pc2",
        "commands":[
            "ip address add 192.168.2.222/24 dev eth0",
            "ip -6 address add fd00:2::222/64 dev eth0",
            "ip route add default via 192.168.2.254",
            "ip -6 route add default via fd00:2::254"
        ]
    },
    {
        "machine_name": "dnsroot",
        "commands":[
            "ip address add 192.168.0.5/24 dev eth0",
            "ip -6 address add fd00:0::5/64 dev eth0",
            "ip route add default via 192.168.0.254",
            "ip -6 route add default via fd00:0::254",
            "systemctl start bind9"
        ] 
    },
    {
        "machine_name": "localuni",
        "commands":[
            "ip address add 192.168.1.110/24 dev eth0",
            "ip -6 address add fd00:1::110/64 dev eth0",
            "ip route add default via 192.168.1.254",
            "ip -6 route add default via fd00:1::254",
            "systemctl start bind9"
        ] 
    },
    {
        "machine_name": "localstart",
        "commands":[
            "ip address add 192.168.2.220/24 dev eth0",
            "ip -6 address add fd00:2::220/64 dev eth0",
            "ip route add default via 192.168.2.254",
            "ip -6 route add default via fd00:2::254",
            "systemctl start bind9"
        ] 
    },
        {
        "machine_name": "dnsuni",
        "commands":[
            "ip address add 192.168.1.11/24 dev eth0",
            "ip -6 address add fd00:1::11/64 dev eth0",
            "ip route add default via 192.168.1.254",
            "ip -6 route add default via fd00:1::254",
            "systemctl start bind9"
        ] 
    }, 
    {
        "machine_name": "dnsstart",
        "commands":[
            "ip address add 192.168.2.22/24 dev eth0",
            "ip -6 address add fd00:2::22/64 dev eth0",
            "ip route add default via 192.168.2.254",
            "ip -6 route add default via fd00:2::254",
            "systemctl start bind9"
        ]
    },
        {
        "machine_name":"dnsit",
        "commands":[
            "ip address add 192.168.0.1/24 dev eth0",
            "ip -6 address add fd00:0::1/64 dev eth0",
            "ip route add default via 192.168.0.254",
            "ip -6 route add default via fd00:0::254",
            "systemctl start bind9"
        ]
    },
    {
        "machine_name":"dnsnet",
        "commands":[
            "ip address add 192.168.0.2/24 dev eth0",
            "ip -6 address add fd00:0::2/64 dev eth0",
            "ip route add default via 192.168.0.254",
            "ip -6 route add default via fd00:0::254",
            "systemctl start bind9"
        ]
    }
]

named_base = 'options { directory "/var/cache/bind"; allow-query { any; }; allow-recursion { any; }; dnssec-validation no; };\n'

db_root_hints = ". 3600000 IN NS dnsroot.\ndnsroot. 3600000 IN A 192.168.0.5\ndnsroot. 3600000 IN AAAA fd00:0::5\n"

soa_std = "1 604800 86400 2419200 604800"

dns_config = [
    {
        "machine_name": "pc1",
        "files": [
            {"path": "/etc/resolv.conf", 
             "content": "nameserver 192.168.1.110\nnameserver fd00:1::110\nsearch uniroma3.it"
            }
        ]
    },
    {
        "machine_name": "pc2",
        "files": [
            {"path": "/etc/resolv.conf", 
             "content": "nameserver 192.168.2.220\nnameserver fd00:2::220\nsearch startup.net"
            }
        ]
    },
    {
        "machine_name": "dnsroot",
        "files": [
            {"path": "/etc/bind/named.conf", 
             "content": named_base + 'zone "." { type master; file "/etc/bind/db.root_zone"; };'},

            {"path": "/etc/bind/db.root_zone", 
             "content": f"$TTL 60000\n@ IN SOA dnsroot. root.dnsroot. ({soa_std})\n@ IN NS dnsroot.\ndnsroot. IN A 192.168.0.5\ndnsroot. IN AAAA fd00:0::5\nit. IN NS dnsit.it.\ndnsit.it. IN A 192.168.0.1\ndnsit.it. IN AAAA fd00:0::1\nnet. IN NS dnsnet.net.\ndnsnet.net. IN A 192.168.0.2\ndnsnet.net. IN AAAA fd00:0::2\n"}
        ]
    },
    {
        "machine_name": "dnsit",
        "files": [
            {"path": "/etc/bind/named.conf", 
             "content": named_base + 'zone "it" { type master; file "/etc/bind/db.it"; };'},

            {"path": "/etc/bind/db.it", 
             "content": f"$TTL 60000\n@ IN SOA dnsit.it. root.dnsit.it. ({soa_std})\n@ IN NS dnsit.it.\ndnsit.it. IN A 192.168.0.1\ndnsit.it. IN AAAA fd00:0::1\nuniroma3.it. IN NS dnsuni.uniroma3.it.\ndnsuni.uniroma3.it. IN A 192.168.1.11\ndnsuni.uniroma3.it. IN AAAA fd00:1::11\n"}
        ]
    },
    {
        "machine_name": "dnsnet",
        "files": [
            {"path": "/etc/bind/named.conf", 
             "content": named_base + 'zone "net" { type master; file "/etc/bind/db.net"; };'},+

            {"path": "/etc/bind/db.net", 
             "content": f"$TTL 60000\n@ IN SOA dnsnet.net. root.dnsnet.net. ({soa_std})\n@ IN NS dnsnet.net.\ndnsnet.net. IN A 192.168.0.2\ndnsnet.net. IN AAAA fd00:0::2\nstartup.net. IN NS dnsstart.startup.net.\ndnsstart.startup.net. IN A 192.168.2.22\ndnsstart.startup.net. IN AAAA fd00:2::22\n"}
        ]
    },
    {
        "machine_name": "dnsuni",
        "files": [
            {"path": "/etc/bind/named.conf", 
             "content": named_base + 'zone "uniroma3.it" { type master; file "/etc/bind/db.it.uniroma3"; };'},

            {"path": "/etc/bind/db.it.uniroma3", 
             "content": f"$TTL 60000\n@ IN SOA dnsuni.uniroma3.it. root.dnsuni.uniroma3.it. ({soa_std})\n@ IN NS dnsuni.uniroma3.it.\ndnsuni.uniroma3.it. IN A 192.168.1.11\ndnsuni.uniroma3.it. IN AAAA fd00:1::11\npc1.uniroma3.it. IN A 192.168.1.111\npc1.uniroma3.it. IN AAAA fd00:1::111\n"}
        ]
    },
    {
        "machine_name": "dnsstart",
        "files": [
            {"path": "/etc/bind/named.conf", 
             "content": named_base + 'zone "startup.net" { type master; file "/etc/bind/db.net.startup"; };'},

            {"path": "/etc/bind/db.net.startup", 
             "content": f"$TTL 60000\n@ IN SOA dnsstart.startup.net. root.dnsstart.startup.net. ({soa_std})\n@ IN NS dnsstart.startup.net.\ndnsstart.startup.net. IN A 192.168.2.22\ndnsstart.startup.net. IN AAAA fd00:2::22\npc2.startup.net. IN A 192.168.2.222\npc2.startup.net. IN AAAA fd00:2::222\n"}
        ]
    },
    {
        "machine_name": "localuni",
        "files": [
            {"path": "/etc/bind/named.conf", 
             "content": named_base + 'zone "." { type hint; file "/etc/bind/db.root"; };'},

            {"path": "/etc/bind/db.root", 
             "content": db_root_hints}
        ]
    },
    {
        "machine_name": "localstart",
        "files": [
            {"path": "/etc/bind/named.conf", 
             "content": named_base + 'zone "." { type hint; file "/etc/bind/db.root"; };'},
             
            {"path": "/etc/bind/db.root", 
             "content": db_root_hints}
        ]
    }
]

def test_scenario():
    session = requests.Session()
    lab_name = "lab_Scenario"
    try:
        print("Creating lab...")
        response = session.post(f"{URL_SERVER}/lab/create", json={"lab_name":lab_name})
        assert response.status_code == 200, f"Failed to create {lab_name}: {response.text}"
        print(f"Lab '{lab_name}' created.")

        print("Machines creation...")
        for machine in machines:
            response = session.post(f"{URL_SERVER}/lab/machine", params = {"lab_name": lab_name},json = {"name": machine, "meta":{"ipv6":True}})
            assert response.status_code == 200, f"Failed to create {machine}: {response.text}"
            print(f"Machine '{machine}' created.")
        
        print("Setting up machines' interfaces...")
        for iface in interfaces:
            response = session.post(f"{URL_SERVER}/lab/machine/interface", params = {"lab_name":lab_name, "machine_name": iface["machine"], "domain" :iface["domain"]})
            assert response.status_code ==200, f"Falied to set interface for {iface['machine']}: {response.text}"
            print(f"Interface for {iface['machine']} set in domain {iface['domain']}")
        
        print("Stratup configuration loading...")
        for config in startup:
            response = session.post(f"{URL_SERVER}/lab/machine/startup", params = {"lab_name": lab_name}, json = config)
            assert response.status_code == 200, f"Failed to apply startup config for {config['machine_name']}: {response.text}"
            print(f"{config['machine_name']}: configuration applied.")

        print("DNS configuration loading...")
        for config in dns_config:
            response = session.post(f"{URL_SERVER}/lab/machine/file/string", params = {"lab_name": lab_name}, json = config)
            assert response.status_code == 200, f"Failed to apply DNS configuration for {config['machine_name']}:{response.text}"
            print(f"{config['machine_name']}: DNS configuration applied.")
        
        print("Lab deployment loading...")
        response = session.post(f"{URL_SERVER}/lab/deploy", params = {"lab_name" : lab_name})
        assert response.status_code == 200, f"Failed to deploy {lab_name}: {response.text}"
        print(f"'{lab_name}' successfully deployed.")

        time.sleep(30)

        print ("Checking lab machines...")
        response = session.get(f"{URL_SERVER}/lab/machine", params = {"lab_name": lab_name})
        if response.status_code == 200: 
            machines_list = response.json().get(f"Machines in {lab_name}", [])
            print(f"Machines in {lab_name}:{machines_list}")

        print("Checking exec commands...")
        exec_payload = {"machine_name":"pc1", "command": "cat /etc/resolv.conf"}
        response = session.post(f"{URL_SERVER}/lab/exec", params={"lab_name":lab_name}, json = exec_payload)
        json_response = response.json()
        output = json_response.get("output", "")
        assert "nameserver 192.168.1.110" in output, "Test Fallito: nameserver IPv4 mancante in pc1!"
        assert "nameserver fd00:1::110" in output, "Test Fallito: nameserver IPv6 mancante in pc1!"
        assert "search uniroma3.it" in output, "Test Fallito: direttiva search mancante in pc1!"

        assert response.status_code == 200, f"Failed to execute command on pc1: {response.text}"

        exec_ping = {"machine_name" :"pc1", "command": "ping -c 2 fd00:2::222"}
        response = session.post(f"{URL_SERVER}/lab/exec", params={"lab_name":lab_name}, json = exec_ping)
        assert response.status_code == 200, f"Ping command failed"
        json_ping = response.json()
        ping_output = json_ping.get("output", "")
        assert "2 received" in ping_output and "0% packet loss" in ping_output, "Ping test failed"

        exec_dns = {"machine_name":"pc1", "command": "ping -c 4 pc2.startup.net"}
        response = session.post(f"{URL_SERVER}/lab/exec", params={"lab_name":lab_name}, json = exec_dns)
        assert response.status_code == 200, f"Ping command failed"
        exec_json = response.json()
        dns_output = exec_json.get("output", "")
        assert "4 received" in dns_output and "0% packet loss" in dns_output, "Ping test failed"


        exec_dns = {"machine_name" :"pc2", "command": "ping -c 3 pc1.uniroma3.it"}
        response = session.post(f"{URL_SERVER}/lab/exec", params = {"lab_name":lab_name}, json = exec_dns)
        assert response.status_code == 200, f"Ping command failed"
        exec_json = response.json()
        dns_output = exec_json.get("output", "")
        assert "3 received" in dns_output and "0% packet loss" in dns_output, "Ping test failed"

        print("Exec commands tests work properly.")

        print("Undeploying lab..")
        response = session.post(f"{URL_SERVER}/lab/undeploy", params = {"lab_name" : lab_name})
        assert response.status_code == 200, f"Failed to undeploy the lab: {response.text}"

    except Exception as e: raise Exception(f"{str(e)}")
    except AssertionError as ae: raise Exception(f"{str(ae)}")



if __name__ == "__main__": test_scenario()
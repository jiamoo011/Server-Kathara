import requests

url = "http://127.0.0.1:5000"

nome_lab = "labDNS"

response_deploy = requests.post(f"{url}/lab/deploy", params={"lab_name": nome_lab})

print(response_deploy.json())


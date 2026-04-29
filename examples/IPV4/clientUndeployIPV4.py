import requests

url = "http://127.0.0.1:5000"

nome_lab = "lab1"

response_undeploy = requests.post(f"{url}/lab/undeploy", params={"lab_name": nome_lab})

print(response_undeploy.json())
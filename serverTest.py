import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from Server import app, labs_storage

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_storage(): labs_storage.clear()

def test_create_lab_success():
    response = client.post("/lab/create", json={"lab_name": "test_lab"})
    assert response.status_code == 200
    assert response.json() == {"message": "test_lab created successfully"}
    assert "test_lab" in labs_storage

def test_create_lab_duplicate_error():
    client.post("/lab/create", json={"lab_name": "test_lab"})
    response = client.post("/lab/create", json={"lab_name": "test_lab"})
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_list_labs():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/create", json={"lab_name": "lab2"})
    response = client.get("/lab")
    assert response.status_code == 200
    assert "lab1" in response.json()["List of labs"]
    assert "lab2" in response.json()["List of labs"]

def test_new_machine_success():
    client.post("/lab/create", json={"lab_name": "lab1"})
    response = client.post("/lab/machine?lab_name=lab1", json={"name": "pc1", "meta": {"ipv6": False}})
    assert response.status_code == 200
    assert "pc1 created successfully" in response.json()["message"]

def test_new_machine_lab_not_found():
    response = client.post("/lab/machine?lab_name=ghost", json={"name": "pc1"})
    assert response.status_code == 404
    assert "ghost not found" in response.json()["detail"]

def test_list_machines():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})
    response = client.get("/lab/machine?lab_name=lab1")
    assert response.status_code == 200
    assert "pc1" in response.json()["Machines in lab1"]

def test_deploy_lab_success():
    client.post("/lab/create", json={"lab_name":"lab1"})
    with patch("Server.Kathara") as mock_kathara:
        response = client.post("/lab/deploy?lab_name=lab1")
    if response.status_code != 200:
        print(response.status_code, response.text)
    assert response.status_code == 200
    assert "deployed successfully" in response.json().get("message", "")

def test_deploy_lab_not_found():
    response = client.post("/lab/deploy?lab_name=lab3")
    assert response.status_code == 404

def test_undeploy_lab_success():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/deploy?lab_name=lab1")
    response = client.post("/lab/undeploy?lab_name=lab1")
    assert response.status_code == 200

def test_undeploy_lab_not_found():
    response = client.post("/lab/undeploy?lab_name=nonexistent")
    assert response.status_code == 404

def test_startup_file_success():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})     
    payload = {"machine_name": "pc1", "commands": ["ip address add 195.11.14.5/24 dev eth0", "ip link set dev eth0 up"]}
    response = client.post("/lab/machine/startup?lab_name=lab1", json=payload)
    assert response.status_code == 200
    assert "Startup configuration applied" in response.json()["message"]

def test_startup_file_machine_not_found():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})     
    payload = {"machine_name": "pc2", "commands": ["ip address add 195.11.14.5/24 dev eth0", "ip link set dev eth0 up"]}
    response = client.post("/lab/machine/startup?lab_name=lab1", json=payload)
    assert response.status_code == 404

def test_device_file_from_string_success():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})
    
    payload = {"machine_name": "pc1","files": [{"path": "/etc/test.txt", "content": "hello world", "src": None}]}

    response = client.post("/lab/machine/file/string?lab_name=lab1", json=payload)
    assert response.status_code == 200
    assert "/etc/test.txt" in response.json()["files created at this source"]

def test_device_file_from_path_success():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})   
    payload = {"machine_name": "pc1","files": [{"path": "/etc/test.txt", "content": "hello world", "src": "C:/Users/giamm/Documents/Università/Tirocinio/Server/Test/text.txt"}]}
    response = client.post("/lab/machine/file/path?lab_name=lab1", json=payload)
    assert response.status_code == 200

def test_device_file_wrong_path():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})   
    payload = {"machine_name": "pc1","files": [{"path": "/etc/test.txt", "content": "hello world", "src": "C:/Users/giamm/Documents/Università/Tirocinio/Server/Test/hello.txt"}]}
    response = client.post("/lab/machine/file/path?lab_name=lab1", json=payload)
    assert response.status_code == 422

def test_device_file_from_path_missing_src():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})
    payload = {"machine_name": "pc1","files": [{"path": "/etc/dest.txt", "src":None, "content": None}]}
    response = client.post("/lab/machine/file/path?lab_name=lab1", json=payload)
    assert response.status_code == 400
    assert "Source path is required" in response.json()["detail"]

def test_add_interface_success():
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})   
    response = client.post("/lab/machine/interface?lab_name=lab1&machine_name=pc1&domain=A")
    assert response.status_code == 200
    assert response.json()["domain"] == "A"

@patch("Server.Kathara")
def test_exec_success(mock_kathara):
    client.post("/lab/create", json={"lab_name": "lab1"})
    client.post("/lab/machine?lab_name=lab1", json={"name": "pc1"})

    # Non serve chiamare /deploy reale, perché stiamo simulando.
    # Ma se la logica del tuo server lo richiede per qualche flag interno, 
    # puoi chiamarlo (tanto è tutto mockato se usi patch anche lì o se il server non controlla lo stato live).
    
    # 2. Configurazione del Mock
    # Diciamo a Kathara: "Quando ti viene chiesto di fare .exec(), restituisci questi byte"
    mock_instance = mock_kathara.get_instance.return_value
    mock_instance.exec.return_value = [b"bin\n", b"boot\n", b"dev\n"] # Simula l'output di 'ls'

    # 3. Esecuzione della chiamata
    payload = {"machine_name": "pc1", "command": "ls"}
    response = client.post("/lab/exec?lab_name=lab1", json=payload)

    # 4. Verifiche
    assert response.status_code == 200
    # Verifica che l'output simulato sia presente nella risposta JSON
    assert "bin" in response.json()["output"]

def test_exec_machine_not_found():
    client.post("/lab/create", json={"lab_name": "lab1"})
    payload = {"machine_name": "ghost", "command": "ls"}
    response = client.post("/lab/exec?lab_name=lab1", json = payload)
    assert response.status_code == 404
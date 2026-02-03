The following project implements a **Client-Server** system for the programmatic management of virtual network labs based on Kathara.

Prerequisites required for execution:
- **Python 3.8+**
- **Docker/desktop (running)**
- **Kathara (core and API)**

In the project folder, run the command **pip install -r requirements.txt** to install the necessary libraries.

Following to that, in order to start the server, run the following command in the terminal: **uvicorn Server:app --reload --port 5000**

After starting the server, go to the clients folder from the main folder using the command **cd clients** and execute the mainClient.py file with **python3 mainClient.py**. The server will be started.

# Server Error Codes:

**200** | Operation successful. | No error. |
**400** | Server cannot process the client request. | Wrong syntax or missing data. | 
**404** | Server processed the request but cannot find the client resource. | 
**422** | Server understood the client request but cannot process it due to semantic errors in the sent data. | 
**500** | Internal Server Error. | Server cannot communicate with Docker or Kathara. |

The system is divided into two logical components:

1. **Server API (Backend)**: A RESTful interface (based on FastAPI) that abstracts the complexity of Docker and the Kathara Framework.

2. **Clients**: Python language scripts that define the network topology, configure network devices, and send commands to the server.

## Project structure: 

The project follows a clear separation between management logic (Server) and topology definition (Clients).

├── Server.py                         # [Backend] FastAPI Server API & Kathara Logic written in Python
├── requirements.txt                  # Python dependencies needed to use the server
├── README.md                         # Project documentation
├── Test
│   ├── serverTest.py                 # Script in which every endpoint is tested, and every result is showed
└── clients                  
    ├── DNS
    │   ├── clientDns.py              # Defines DNS network topology and configurations 
    │   │                              (it uses machine.create_file_from_string)
    │   ├── clientDns2.0.py           # Defines the same DNS network topology version
    │   │                              (it uses machine.create_file_from_string)
    │   ├── clientDeployDns.py        # Quick Python script for DNS lab deployment
    │   └── clientUndeployDns.py      # Quick Python script for DNS lab undeployment
    └── IPV4
        ├── clientIPV4.py             # Defines machines, configures domains and IP addresses
        ├── clientDeployIPV4.py       # Quick Python script for IPV4 lab deployment
        └── clientUndeployIPV4.py     # Quick Python script for IPV4 lab undeployment

To view all available endpoints without having to write scripts, you can access **http://127.0.0.1:5000/docs** via browser. It is a debugging REST Client that can verify that the APIs are responding correctly. From every created endpoint, clicking on "Try it out" allows you to execute the request.

The Server presents the following endpoints:

**Lab creation** : (@app.post("/lab/create"))
Before creating the lab, a check is performed: if the lab name exists in labs_storage, a 400 exception is raised. Otherwise, a lab object is created with the entered name and inserted into labs_storage.

**Lab deploy** : (@app.post("/lab/deploy"))
Before deploying the lab, passed via a lab_name string, a check is performed. If it is not found in labs_storage, the lab object is retrieved via the hash using the method Kathara.get_instance().get_lab_from_api(lab_name = lab_name); otherwise, a 404 exception is raised. A further 400 exception is raised if the lab has no machines to deploy, and a general 500 exception.

**Lab undeploy**: (@app.post("/lab/undeploy"))
A lab_name string is passed to select the lab; if it is not present in labs_storage, a 400 exception is raised. The undeploy is performed via the method Kathara.get_instance().undeploy_lab(lab_name = nameOfLab); otherwise, a 500 exception is raised.

**Machine Creation**: @app.post("/lab/machine")
The parameters include the string of the lab name where they must be added and a MachineRequest data structure with a name and meta field. If the lab is not present, a 404 exception is raised. Using the lab's new_machine method, the machines are created returning a success message; otherwise, a 500 exception is raised.

**Adding an interface to a machine**: @app.post("/lab/machine/interface")
I pass a lab_name string, a machine_name string, and a string for the domain as parameters. There are initially two checks verifying the presence of the lab and, if successful, the presence of the machine in the lab; otherwise, a 404 exception is raised for both. The method used to set the interface is given by the lab method connect_machine_to_link(machineName, domainString); a 500 exception is raised if the operation is not successful.

**Creation of startup files for a lab's machines**: @app.post("/lab/machine/startup")
The endpoint has the lab_name string and a MachineStartupRequest data structure as parameters, which presents 3 fields: a machineName string, a list of strings for commands, and a string for a machine's startup file. Initial checks verify the presence of the lab in labs_storage and subsequently the presence of the machine in the lab; if the checks fail, 404 exceptions will be raised. The startup file is named as follows: "{machineName}.startup". Subsequently, you create a "textFile" string in which you insert the commands. Once the machine is selected from the chosen lab, I generate the startup file via the create_startup_file_from_string() method, passing the machine and the text file as parameters. If the file creation is not successful, a 422 exception is raised if data is missing, or 500 for an internal server error.

**File creation in machines' path (machine.create_file_from_string method)**: @app.post("/lab/machine/file/string")
The endpoint has the lab_name string and a CreateFileRequest data structure, in which there are three string parameters: two are Optional (src and content) and one is standard (path). Before creating the file, you have to verify the presence of the lab and the machine in which you want to create the file. Otherwhise a 404 exception is raised.
Inside the try block the machine instance is retrieved from the lab using the provided machine name. The system initializes a list to track the created files and iterates through the list of file configurations provided in the request body. For each item, the Kathara method machine.create_file_from_string(file.content, file.path) is invoked to inject the content directly into the specified path within the virtual machine. The path is then appended to the list of created files. Finally, the endpoint returns a JSON response containing a success message and the list of the files successfully generated.
If any error occurs during this process, a 422 exception or a 500 exception is raised depending on the nature of the error.

**File creation in machines' path (machine.create_file_from_string method)**: @app.post("/lab/machine/file/path")
This endpoint is the same as the one written above. The only thing that changes is that in the try the method machine.create_file_from_path is used. It has only two parameters, the source from which the content of a file is copied and the file's path destination for this content.

**Execution of commands**: @app.post("/lab/exec")
The exec has the lab_name string and an ExeCommandRequest data structure as parameters. I verify the presence of the lab in labs_storage; otherwise, a 404 exception is raised. Once the Lab object is retrieved, I check if the machine from which I want to run exec exists in the lab. A .lower() function is also executed on the machine name in case the machine name is sent in CAPS LOCK as input. A 404 exception will be raised if the machine is not present in the lab. Once the machine object is retrieved, the exec (machine_name=machine.name, command=er.command, lab_name=lab.name, stream=False) is executed in a try block. The parameters are: the machine name, the list of commands, the lab name, and a stream boolean initialized to false as we do not want to open a continuous stream but only obtain a generator with the command results as output. For every line of output produced by the command, the format is verified in a try block; if they are in bytes or another format, they are decoded into a string and added to the final output; if they are other strings, they are added to the final output. If there are decoding errors for a line, it ignores it and continues with the next one, instead of crashing the server. If errors are caught in the first try block, a 500 exception with the detailed exception message is returned to the client.

**Print the list of machines in a lab**: @app.get("/lab/machine")
A lab_name string is sent to the endpoint to select the lab. The presence of the lab in labs_storage is verified first; otherwise, a 404 exception is raised. If the check passes, the lab object is retrieved and the list of the lab's machines is returned with the method "list(lab.machines.keys())".

**Print existing labs**: @app.get("/lab")
To return the list of existing labs, I extract the labs_storage keys via the method: list(labs_storage.keys())

The serverTest file presents 16 different test. You can run it with this command in the prompt : **pytest -s -v serverTest.py**.

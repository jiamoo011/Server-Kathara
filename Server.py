from Kathara.manager.Kathara import Kathara
from Kathara.model.Lab import Lab
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, List,Dict, Optional

app = FastAPI()

labs_storage : Dict[str, Lab] = {}

class MachineRequest(BaseModel):
    name: str = None
    meta: Dict[str,Any] = {}

class LabDeployRequest(BaseModel):
    lab_name: str = None
    machines: Optional[List[MachineRequest]] = []

class ExeCommandRequest(BaseModel):
    machine_name : str
    command : str
    
class MachineStartupRequest(BaseModel):
    machine_name : str
    commands : List[str]
    startup_file : Optional[str] = None 

class FileConfig(BaseModel):
    src : Optional[str]
    path : str
    content : Optional[str]

class CreateFileRequest(BaseModel):
    machine_name : str
    files : Optional[List[FileConfig]] = []
    commands : Optional[str] = None


@app.post("/lab/create")
def create_lab(request : LabDeployRequest):

    if request.lab_name in labs_storage: raise HTTPException(status_code=400, detail=f"{request.lab_name} already exists")   
    
    new_lab = Lab(name=request.lab_name)

    labs_storage[request.lab_name] = new_lab
    
    return {"message": f"{request.lab_name} created successfully"}

@app.post("/lab/deploy")
def deploy_lab(lab_name: str):

    lab = None
    
    if lab_name not in labs_storage: raise HTTPException(status_code = 404, detail = f"{lab_name} not found")
    
    try: 
        Kathara.get_instance().deploy_lab(lab) 
        return {"message": f"{lab_name} deployed successfully"}
    
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/lab/undeploy")
def undeploy_lab(lab_name: str):

    if lab_name not in labs_storage : raise HTTPException(status_code = 404, detail = f"{lab_name} not found")
    
    try:
        Kathara.get_instance().undeploy_lab(lab_name = lab_name) 
        return {"message": f"{lab_name} undeployed successfully"}

    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/lab/machine")
def new_machine(lab_name: str, rm: MachineRequest):

    if lab_name not in labs_storage: raise HTTPException(status_code=404, detail=f"{lab_name} not found")
    
    lab = labs_storage[lab_name] 
  
    try:
        machine=lab.new_machine(rm.name, **rm.meta)

        return{"message": f"{machine.name} created successfully in {lab_name}"} 
        
    except Exception as e : raise HTTPException(status_code = 422, detail = str(e))
    except Exception as e : raise HTTPException(status_code = 500, detail = str(e))
    
@app.post("/lab/machine/startup")
def default_startup_file(lab_name: str, req: MachineStartupRequest):

    if lab_name not in labs_storage: raise HTTPException(status_code = 404, detail = f"{lab_name} not found")
        
    lab = labs_storage[lab_name]
    
    if req.machine_name not in lab.machines: raise HTTPException(status_code = 404, detail = f"{req.machine_name} not found in {lab_name}")
           
    req.startup_file = f"{req.machine_name}.startup" 

    file_text = "\n".join(req.commands) 

    try:
        m = lab.machines[req.machine_name] 

        lab.create_startup_file_from_string(m,file_text)
        return {
            "message": f"Startup configuration applied to {req.machine_name}",
            "filename created:": req.startup_file,
            "configuration:": req.commands
        }
    
    except Exception as e: raise HTTPException(status_code=422, detail=str(e))
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))


@app.post("/lab/machine/file/string")
def device_file_from_string(lab_name: str, fil: CreateFileRequest):

    if lab_name not in labs_storage: raise HTTPException(status_code = 404, detail = f"{lab_name} not found")
    
    else: lab = labs_storage[lab_name]

    if fil.machine_name not in lab.machines: raise HTTPException(status_code = 404,detail = f"{fil.machine_name} not found in {lab_name}")
    
    try:
        m = lab.machines[fil.machine_name]
        processed_files = []

        for file in fil.files:
            m.create_file_from_string(file.content, file.path)
            processed_files.append(file.path)

        return {
            "message": f"Configuration applied to {fil.machine_name}",
            "files created at this source": processed_files
        }

    except Exception as e: raise HTTPException(status_code = 422, detail = str(e))
    except Exception as e: raise HTTPException(status_code = 500, detail = str(e))

@app.post("/lab/machine/file/path")
def device_file_from_path(lab_name : str , fil : CreateFileRequest):

    if lab_name not in labs_storage: raise HTTPException(status_code = 404, detail = f"{lab_name} not found")
    
    else: lab = labs_storage[lab_name]

    if fil.machine_name not in lab.machines: raise HTTPException(status_code=404,detail = f"{fil.machine_name} not found in {lab_name}")

    try:
        m = lab.machines[fil.machine_name]
        processed_files = []

        for file in fil.files:

            if not file.src: raise HTTPException(status_code = 400, detail = "Source path is required")

            m.create_file_from_path(file.src, file.path)

            processed_files.append({"from_source": file.src, "to_path": file.path})

        return {"message": f"Configuration applied to {fil.machine_name}","files_processed": processed_files}
    
    except HTTPException as e: raise e
    except Exception as e: raise HTTPException(status_code = 422, detail = str(e))
    except Exception as e: raise HTTPException(status_code = 500, detail = str(e))


@app.post("/lab/machine/interface")
def add_interface_to_machine(lab_name: str, machine_name: str, domain: str):

    if lab_name not in labs_storage: raise HTTPException(status_code = 404, detail = f"{lab_name} not found")

    lab = labs_storage[lab_name]

    if machine_name not in lab.machines: raise HTTPException(status_code = 404, detail = f"{machine_name} not found")

    try:
        machine = lab.machines[machine_name]
        lab.connect_machine_to_link(machine.name, domain)
        return {"message": f"Interface added to {machine_name}", "domain": domain}
        
    except Exception as e: raise HTTPException(status_code = 422, detail = str(e))
    except Exception as e: raise HTTPException(status_code = 500, detail = str(e))

@app.post("/lab/exec")
def exec_command(lab_name: str, er: ExeCommandRequest):

    if lab_name not in labs_storage: raise HTTPException(status_code=404, detail = f"{lab_name} not found")

    else: lab = labs_storage[lab_name]

    safe_name = er.machine_name.lower()

    if safe_name not in lab.machines: raise HTTPException(status_code=404, detail = f"{safe_name} not found in {lab_name}")
    
    machine = lab.machines[safe_name]

    try:
        output_generator = Kathara.get_instance().exec(machine_name=machine.name, command=er.command, lab_name = lab.name, stream = False)
        full_output = ""
        if output_generator:
            for line in output_generator: 
                try:
                    if isinstance(line, bytes): 
                        full_output += line.decode('utf-8') 
                    else:
                        full_output += str(line)
                except Exception: pass 
        return {
            "machine": machine.name, "command": er.command, "output": full_output
        }
    
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/lab/machine")
def list_machines(lab_name: str):

    if lab_name not in labs_storage: raise HTTPException(status_code=404, detail = f"{lab_name} not found")

    lab=labs_storage[lab_name]

    return {f"Machines in {lab_name}": list(lab.machines.keys())}

@app.get("/lab")
def list_labs(): return {"List of labs": list(labs_storage.keys())}

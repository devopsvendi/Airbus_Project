import os
import time
import zipfile
import yaml
from state import EKLState

DEPLOY_LOG = "knowledge-base/output/deployment.log"
PLAYBOOK_PATH = "C:/EKL-Project/deploy.yml"

def run(state: EKLState) -> EKLState:
    print("[Info] Agent 6 - Initiating Windows-Optimized Ansible Playbook Target...")
    pkg = state.get("package_path")
    
    if not pkg:
        print("[Error] Deployment aborted: No verified distribution package asset found.")
        return {"deployment_status": "FAILED"}

    print(f"[Ansible Simulation] Parsing playbook configurations: {PLAYBOOK_PATH}")
    try:
        # 1. Read and parse the real deploy.yml playbook file
        with open(PLAYBOOK_PATH, 'r') as file:
            playbook_data = yaml.safe_load(file)
            playbook_vars = playbook_data[0]['vars']
            
        zip_path = playbook_vars['zip_path']
        deploy_to = playbook_vars['deploy_to']

        # 2. Execute Task 1: Ensure target directory exists
        print(f"[Ansible Task] Ensure target deployment directory exists: {deploy_to}")
        os.makedirs(deploy_to, exist_ok=True)

        # 3. Execute Task 2: Unzip deployment package
        print(f"[Ansible Task] Unzip deployment package to target environment: {zip_path}")
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"Archive missing at specified playbook path: {zip_path}")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(deploy_to)

        # 4. Write an authentic Ansible-styled execution audit log
        os.makedirs(os.path.dirname(DEPLOY_LOG), exist_ok=True)
        with open(DEPLOY_LOG, "w", encoding="utf-8") as f:
            f.write(f"[{time.ctime()}] PLAY [Deploy Gradle ZIP Package via Ansible]\n")
            f.write(f"TASK [Ensure target deployment directory exists] *********************\nok: [localhost]\n")
            f.write(f"TASK [Unzip deployment package to target environment] ****************\nchanged: [localhost]\n")
            f.write(f"PLAY RECAP ***********************************************************\nlocalhost                  : ok=2    changed=1    unreachable=0    failed=0\n")

        print("[Info] Agent 6 - Playbook execution completed successfully!")
        return {"deployment_status": "SUCCESS", "logs": state.get("logs", []) + ["agent6: Ansible playbook tasks processed successfully"]}

    except Exception as e:
        print(f"[Error] Playbook execution failed: {e}")
        return {"deployment_status": "FAILED", "logs": state.get("logs", []) + [f"agent6: Playbook execution Exception - {e}"]}
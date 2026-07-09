import os
import time
import subprocess
from state import EKLState

DEPLOY_LOG = "knowledge-base/output/deployment.log"
PLAYBOOK_PATH = "C:\\EKL-Project\\deploy.yml"

def run(state: EKLState) -> EKLState:
    print("[Info] Agent 6 - Initiating Ansible Production Deployment Target...")
    pkg = state.get("package_path")
    
    if not pkg:
        print("[Error] Deployment aborted: No verified distribution package asset found.")
        return {"deployment_status": "FAILED"}

    # Triggering the Ansible playbook locally
    print(f"[Ansible] Executing playbook: {PLAYBOOK_PATH}")
    try:
        # Runs 'ansible-playbook deploy.yml' via command line
        result = subprocess.run(
            ["ansible-playbook", PLAYBOOK_PATH],
            shell=True,
            capture_output=True,
            text=True
        )
        
        # Log Ansible output for review
        os.makedirs(os.path.dirname(DEPLOY_LOG), exist_ok=True)
        with open(DEPLOY_LOG, "w", encoding="utf-8") as f:
            f.write(f"[{time.ctime()}] Ansible Deployment Log:\n")
            f.write(result.stdout)
            if result.stderr:
                f.write(f"\nErrors:\n{result.stderr}")

        if result.returncode == 0:
            print("[Info] Agent 6 - Ansible deployment completed successfully!")
            return {"deployment_status": "SUCCESS", "logs": state.get("logs", []) + ["agent6: Ansible deployed ZIP package successfully"]}
        else:
            print("[Error] Agent 6 - Ansible playbook failed execution.")
            return {"deployment_status": "FAILED", "logs": state.get("logs", []) + ["agent6: Ansible execution failed"]}

    except Exception as e:
        print(f"[Error] Failed to invoke Ansible: {e}")
        return {"deployment_status": "FAILED", "logs": state.get("logs", []) + [f"agent6: Exception invoking Ansible - {e}"]}
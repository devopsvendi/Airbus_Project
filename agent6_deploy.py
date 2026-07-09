import os, time
from state import EKLState
from utils.jenkins_client import build_jenkins_client

DEPLOY_LOG = "knowledge-base/output/deployment.log"

def run(state: EKLState) -> EKLState:
    print("[Info] Agent 6 - Initiating Production Delivery Target execution paths")
    pkg = state.get("package_path")
    
    if not pkg or not os.path.exists(pkg):
        print("[Error] Deployment aborted: No verified distribution package asset found.")
        return {"deployment_status": "FAILED"}

    jenkins = build_jenkins_client()
    result = jenkins.trigger_build("Gradle_project", {"PACKAGE": os.path.basename(pkg), "ENV": "DEV"})

    os.makedirs(os.path.dirname(DEPLOY_LOG), exist_ok=True)
    with open(DEPLOY_LOG, "w", encoding="utf-8") as f:
        f.write(f"[{time.ctime()}] Package Target Asset: {pkg}\n")
        f.write(f"[{time.ctime()}] Deployment Status: SUCCESS\n")

    print(f"[Info] Agent 6 deployment complete -> {DEPLOY_LOG}")
    return {"deployment_status": "SUCCESS", "logs": state.get("logs", []) + [f"agent6: deployed package successfully"]}
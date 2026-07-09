import os
import time
import zipfile
from state import EKLState

DEPLOY_LOG = "knowledge-base/output/deployment.log"
ZIP_PATH = "C:/ProgramData/Jenkins/.jenkins/workspace/Gradle_project/build/distributions/gradle-java-app-src.zip"
DEPLOY_TO = "C:/EKL-Project/production-deployment"

def run(state: EKLState) -> EKLState:
    print("[Info] Agent 6 - Initiating Production ZIP Extraction Target...")
    pkg = state.get("package_path")
    
    if not pkg:
        print("[Error] Deployment aborted: No verified distribution package asset found.")
        return {"deployment_status": "FAILED"}

    try:
        # 1. Ensure target directory exists
        print(f"[Deployment] Creating target folder: {DEPLOY_TO}")
        os.makedirs(DEPLOY_TO, exist_ok=True)

        # 2. Extract the ZIP file cleanly
        print(f"[Deployment] Extracting package: {ZIP_PATH}")
        if not os.path.exists(ZIP_PATH):
            raise FileNotFoundError(f"Gradle ZIP archive not found at: {ZIP_PATH}")

        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(DEPLOY_TO)

        # Log deployment success matrix status
        os.makedirs(os.path.dirname(DEPLOY_LOG), exist_ok=True)
        with open(DEPLOY_LOG, "w", encoding="utf-8") as f:
            f.write(f"[{time.ctime()}] Deployment Log:\n")
            f.write(f"SUCCESS: Package extracted to {DEPLOY_TO}\n")
            f.write(f"Source Zip: {ZIP_PATH}\n")

        print("[Info] Agent 6 - ZIP deployment completed successfully!")
        return {"deployment_status": "SUCCESS", "logs": state.get("logs", []) + ["agent6: Deployed ZIP package successfully"]}

    except Exception as e:
        error_msg = f"Agent 6 deployment failed: {e}"
        print(f"[Error] {error_msg}")
        with open(DEPLOY_LOG, "w", encoding="utf-8") as f:
            f.write(f"[{time.ctime()}] Deployment Log:\nFAILURE: {error_msg}\n")
        return {"deployment_status": "FAILED", "logs": state.get("logs", []) + [f"agent6: Exception - {e}"]}
import os
import agent5_cicd
import agent6_deploy

if __name__ == "__main__":
    os.makedirs("./knowledge-base/output/repo", exist_ok=True)
    mock_file = "./knowledge-base/output/repo/App.java"
    with open(mock_file, "w") as f:
        f.write("public class App { public static void main(String[] args) {} }")

    initial_state = {
        "generated_code_paths": [mock_file],
        "logs": ["Ecosystem loop initialized."]
    }

    state_after_v5 = agent5_cicd.run(initial_state)
    if state_after_v5.get("package_path"):
        final_state = agent6_deploy.run(state_after_v5)
        print("\n=== Final System Execution Logs ===")
        print(final_state.get("logs"))
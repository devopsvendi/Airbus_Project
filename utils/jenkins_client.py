import os
import jenkins

class JenkinsClientWrapper:
    def __init__(self):
        self.url = os.getenv("JENKINS_URL", "http://localhost:8080")
        self.user = os.getenv("JENKINS_USER", "admin")
        self.token = os.getenv("JENKINS_TOKEN", "11de3b90327c2f62190f4f78275b398d89")
        self.server = jenkins.Jenkins(self.url, username=self.user, password=self.token)

    def trigger_build(self, job_name, parameters):
        self.server.build_job(job_name, parameters=parameters)
        job_info = self.server.get_job_info(job_name)
        return {"build_number": job_info["nextBuildNumber"]}

    def get_build_info(self, job_name, build_number):
        try:
            return self.server.get_build_info(job_name, build_number)
        except Exception:
            return {"result": "PENDING"}

    def get_build_logs(self, job_name, build_number):
        try:
            return self.server.get_build_log(job_name, build_number)
        except Exception:
            return ""

def build_jenkins_client():
    return JenkinsClientWrapper()
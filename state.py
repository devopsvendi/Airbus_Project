from typing import TypedDict, List, Optional

class EKLState(TypedDict, total=False):
    generated_code_paths: List[str]
    package_path: Optional[str]
    deployment_status: str
    logs: List[str]
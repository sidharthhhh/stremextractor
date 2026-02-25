from typing import Dict

# In-memory storage for task statuses
tasks_status: Dict[str, dict] = {}

def get_task(task_id: str) -> dict:
    if task_id not in tasks_status:
        tasks_status[task_id] = {"status": "queued", "progress": 0.0, "result_file": None, "error": None}
    return tasks_status[task_id]

def update_task(task_id: str, status: str, progress: float = 0.0, result_file: str = None, error: str = None):
    task = get_task(task_id)
    task["status"] = status
    task["progress"] = progress
    if result_file:
        task["result_file"] = result_file
    if error:
        task["error"] = error

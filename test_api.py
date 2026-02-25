import requests
import time
import sys

try:
    resp = requests.post("http://localhost:8000/api/download", json={"url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "startTime": "00:00:00", "endTime": "00:00:05"})
    task_id = resp.json()["task_id"]
    print(f"Task ID: {task_id}")
    while True:
        status = requests.get(f"http://localhost:8000/api/status/{task_id}").json()
        print(status)
        if status["status"] in ["completed", "failed"]:
            if status["status"] == "failed":
                print(requests.get("http://localhost:8000/api/debug/tasks").json()[task_id]["error"])
            break
        time.sleep(1)
except Exception as e:
    print(e)

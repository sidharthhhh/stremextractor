import os
import uuid
import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

from backend.models import DownloadRequest, DownloadResponse, TaskStatus
from backend.state import get_task, update_task, tasks_status
from backend.services.downloader import download_video
from backend.services.processor import process_video
from backend.utils.cleanup import delete_file_after_delay

app = FastAPI(title="Local Video Downloader API")

# Add CORS Middleware to allow requests from local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

def background_download_and_process(request: DownloadRequest, task_id: str):
    """
    Background job to download and optionally process the video.
    """
    try:
        update_task(task_id, status="downloading", progress=0.0)
        
        # 1. Download
        downloaded_file = download_video(str(request.url), task_id, TEMP_DIR)
        
        # 2. Process if needed
        is_processing_needed = request.startTime or request.endTime or request.crop
        
        if is_processing_needed:
            update_task(task_id, status="processing", progress=50.0)
            
            ext = os.path.splitext(downloaded_file)[1]
            processed_file = os.path.join(TEMP_DIR, f"{task_id}_processed{ext}")
            
            crop_args = {}
            if request.crop:
                crop_args = {
                    "crop_width": request.crop.width,
                    "crop_height": request.crop.height,
                    "crop_x": request.crop.x,
                    "crop_y": request.crop.y
                }
                
            process_video(
                input_path=downloaded_file,
                output_path=processed_file,
                start_time=request.startTime,
                end_time=request.endTime,
                **crop_args
            )
            
            # Remove original file if processed exists
            if os.path.exists(processed_file):
                try:
                    os.remove(downloaded_file)
                except Exception as e:
                    print(f"Could not remove original file {downloaded_file}: {e}")
                downloaded_file = processed_file
                downloaded_file = processed_file

        update_task(task_id, status="completed", progress=100.0, result_file=downloaded_file)

    except Exception as e:
        # Downloader sets task state to "failed" mostly, but catch anything here
        update_task(task_id, status="failed", error=str(e))
        print(f"Task {task_id} failed: {e}")

@app.post("/api/download", response_model=DownloadResponse)
async def api_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    
    # Initialize task status
    update_task(task_id, status="queued")
    
    # Send download job to background
    background_tasks.add_task(background_download_and_process, request, task_id)
    
    return DownloadResponse(task_id=task_id)

@app.get("/api/status/{task_id}", response_model=TaskStatus)
async def api_status(task_id: str):
    if task_id not in tasks_status:
        raise HTTPException(status_code=404, detail="Task not found")
        
    task = get_task(task_id)
    return TaskStatus(status=task["status"], progress=task["progress"])

@app.get("/api/file/{task_id}")
async def api_get_file(task_id: str, background_tasks: BackgroundTasks):
    if task_id not in tasks_status:
        raise HTTPException(status_code=404, detail="Task not found")
        
    task = get_task(task_id)
    
    if task["status"] != "completed" or not task.get("result_file"):
        raise HTTPException(status_code=400, detail="File is not ready yet")
        
    filepath = task["result_file"]
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File has been deleted or cannot be found")
        
    filename = f"video_{task_id}{os.path.splitext(filepath)[1]}"
    
    # Assign cleanup in background after delivering the file
    background_tasks.add_task(delete_file_after_delay, filepath, 5)  # delete 5 seconds after download finishes
    
    return FileResponse(path=filepath, filename=filename, media_type='application/octet-stream')

@app.get("/api/debug/tasks")
async def debug_tasks():
    from backend.state import tasks_status
    return tasks_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

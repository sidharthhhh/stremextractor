from pydantic import BaseModel, HttpUrl
from typing import Optional

class DownloadRequest(BaseModel):
    url: HttpUrl
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    isVertical: Optional[bool] = False
    format: Optional[str] = "mp4"

class DownloadResponse(BaseModel):
    task_id: str

class TaskStatus(BaseModel):
    status: str
    progress: float

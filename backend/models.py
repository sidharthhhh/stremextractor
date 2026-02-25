from pydantic import BaseModel, HttpUrl
from typing import Optional

class CropOptions(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    x: Optional[int] = None
    y: Optional[int] = None

class DownloadRequest(BaseModel):
    url: HttpUrl
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    crop: Optional[CropOptions] = None

class DownloadResponse(BaseModel):
    task_id: str

class TaskStatus(BaseModel):
    status: str
    progress: float

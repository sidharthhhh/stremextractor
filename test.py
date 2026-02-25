import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.downloader import download_video
try:
    print("Starting download...")
    result = download_video("https://www.youtube.com/watch?v=jNQXAC9IVRw", "test_task_123", "backend/temp")
    print(f"Success! Saved to {result}")
except Exception as e:
    print(f"FAILED: {e}")

import os
import asyncio

async def delete_file_after_delay(filepath: str, delay_seconds: int = 60 * 10):
    await asyncio.sleep(delay_seconds)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            print(f"Deleted temp file: {filepath}")
        except Exception as e:
            print(f"Failed to delete {filepath}: {e}")

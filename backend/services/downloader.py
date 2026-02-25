import yt_dlp
import os
import uuid
from backend.state import update_task

def download_video(url: str, task_id: str, output_dir: str) -> str:
    """
    Downloads the video to the specified directory and updates progress via progress_hook.
    Returns the file path of the downloaded video.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Standard output template
    outtmpl = os.path.join(output_dir, f"{task_id}.%(ext)s")
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            try:
                # Calculate progress percentage
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    pct = (downloaded / total) * 100
                    update_task(task_id, status='downloading', progress=round(pct, 2))
                else:
                    # Fallback if size is unknown
                    update_task(task_id, status='downloading', progress=10.0)
            except Exception as e:
                pass
        elif d['status'] == 'finished':
            update_task(task_id, status='processing', progress=100.0)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': outtmpl,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # if merge_output_format changed extension, handle it:
            if filename.endswith('.webm'):
                 filename = filename.replace('.webm', '.mp4')
            elif filename.endswith('.mkv'):
                 filename = filename.replace('.mkv', '.mp4')
            
            # Since Outtmpl will dictate the path mostly
            ext = info.get('ext', 'mp4')
            result_file = os.path.join(output_dir, f"{task_id}.mp4")
            
            # find actual file if different
            if not os.path.exists(result_file):
                 for root, dirs, files in os.walk(output_dir):
                     for f in files:
                         if f.startswith(task_id) and f.endswith(".mp4"):
                             return os.path.join(root, f)
                             
            return result_file
    except Exception as e:
        import time
        # Handle Windows yt-dlp merge temp rename error
        if "WinError 32" in str(e) and ".temp.mp4" in str(e):
            time.sleep(1) # wait for antivirus/ffmpeg lock to release
            temp_file = os.path.join(output_dir, f"{task_id}.temp.mp4")
            final_file = os.path.join(output_dir, f"{task_id}.mp4")
            if os.path.exists(temp_file):
                try:
                    os.rename(temp_file, final_file)
                    return final_file
                except:
                    return temp_file # fallback to temp file if still locked
            elif os.path.exists(final_file):
                return final_file
                
        update_task(task_id, status='failed', error=str(e))
        raise e

import ffmpeg
import os
from typing import Optional

def process_video(
    input_path: str, 
    output_path: str, 
    start_time: Optional[str] = None, 
    end_time: Optional[str] = None, 
    is_vertical: Optional[bool] = False,
    format: Optional[str] = "mp4"
) -> str:
    input_kwargs = {}
    if start_time:
        input_kwargs['ss'] = start_time.replace('.', ':')
    if end_time:
        input_kwargs['to'] = end_time.replace('.', ':')

    stream = ffmpeg.input(input_path, **input_kwargs)
    
    is_audio_only = format in ["mp3", "wav"]
    if is_audio_only:
        stream = stream.audio # isolate audio stream only
        reencode_video = False
    else:
        reencode_video = (format != "mp4")
        # If vertical crop is requested
        if is_vertical:
            reencode_video = True
            # Crops to 9:16 aspect ratio from the center automatically
            stream = ffmpeg.filter(stream, 'crop', 'ih*9/16', 'ih')

    output_kwargs = {}
    
    if format == "mp3":
        output_kwargs['acodec'] = 'libmp3lame'
    elif format == "wav":
        output_kwargs['acodec'] = 'pcm_s16le'
    elif format == "webm":
        output_kwargs['vcodec'] = 'libvpx-vp9'
        output_kwargs['acodec'] = 'libopus'
    elif format == "mp4_h264":
        output_kwargs['vcodec'] = 'libx264'
        output_kwargs['acodec'] = 'aac'
    else: # pure mp4
        if reencode_video:
            output_kwargs['vcodec'] = 'libx264'
            output_kwargs['acodec'] = 'aac'
        else:
            output_kwargs['c'] = 'copy'

    stream = ffmpeg.output(stream, output_path, **output_kwargs)
    
    try:
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        return output_path
    except FileNotFoundError:
        print("FFmpeg error: FFmpeg is not installed or not added to your system PATH.")
        raise Exception("FFmpeg is missing from the system environment")
    except ffmpeg.Error as e:
        err_msg = e.stderr.decode() if e.stderr else str(e)
        print(f"FFmpeg error: {err_msg}")
        raise Exception(f"Failed to process video: {err_msg}")

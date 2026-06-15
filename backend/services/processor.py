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
        final_stream = stream.audio # isolate audio stream only
        reencode_video = False
    else:
        video_stream = stream.video
        audio_stream = stream.audio
        reencode_video = (format != "mp4")
        
        # If vertical format is requested
        if is_vertical:
            reencode_video = True
            
            # Create a blurred background: scale up to cover 1080x1920, crop center, blur
            bg = ffmpeg.filter(video_stream, 'scale', 1080, 1920, force_original_aspect_ratio='increase')
            bg = ffmpeg.filter(bg, 'crop', 1080, 1920)
            bg = ffmpeg.filter(bg, 'boxblur', 20, 20)
            
            # Create the foreground: scale down to fit inside 1080x1920
            fg = ffmpeg.filter(video_stream, 'scale', 1080, 1920, force_original_aspect_ratio='decrease')
            
            # Overlay foreground over background
            video_stream = ffmpeg.overlay(bg, fg, x='(main_w-overlay_w)/2', y='(main_h-overlay_h)/2')
            
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

    if is_audio_only:
        out = ffmpeg.output(final_stream, output_path, **output_kwargs)
    else:
        out = ffmpeg.output(video_stream, audio_stream, output_path, **output_kwargs)
    
    try:
        ffmpeg.run(out, overwrite_output=True, quiet=True)
        return output_path
    except FileNotFoundError:
        print("FFmpeg error: FFmpeg is not installed or not added to your system PATH.")
        raise Exception("FFmpeg is missing from the system environment")
    except ffmpeg.Error as e:
        err_msg = e.stderr.decode() if e.stderr else str(e)
        print(f"FFmpeg error: {err_msg}")
        raise Exception(f"Failed to process video: {err_msg}")

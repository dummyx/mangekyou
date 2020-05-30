from pathlib import Path
import subprocess
import sys
from fractions import Fraction

preset = 'veryslow'
crf = '14.5'

def b4ke(video_file,subtitle_file):
    output_file = '[BE4K20K]'+video_file.name[:video_file.name.rfind('.')]+'.mp4'
    keyint = int(get_framerate(video_file))*10
    ffmpeg_arg = ['ffmpeg',
                          '-i',str(video_file),
                          '-c:a','aac',
                          '-ar','44100',
                          '-b:a','320k',
                          '-vf','ass=%s'%str(subtitle_file),
                          '-c:v','libx264',
                          '-preset',preset,
                          '-crf', crf,
                          '-x264-params','vbv-maxrate=20000:vbv-bufsize=20000:keyint=%d'%keyint,
                          output_file]
    subprocess.run(ffmpeg_arg)

def get_framerate(video_file):
    ffprobe_arg = ['ffprobe', 
                            '-v','error',
                            '-select_streams','v',
                            '-of','default=noprint_wrappers=1:nokey=1',
                            '-show_entries', 'stream=r_frame_rate',
                            video_file]
    ffprobe_run = subprocess.run(ffprobe_arg,capture_output=True)
    framerate = float(Fraction(ffprobe_run.stdout.decode()))
    return framerate

if __name__=='__main__':
    if len(sys.argv)==3:
        video_file = Path(sys.argv[1])
        subtitle_file = Path(sys.argv[2])
    else:
        vid = input('拖拽视频文件或输入路径\n')
        sub = input('拖拽字幕文件或输入路径\n')
        video_file = Path(vid)
        subtitle_file = Path(sub)
    
    b4ke(video_file,subtitle_file)
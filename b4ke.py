# -*- coding: UTF-8 -*-
import os
import subprocess
import sys
from fractions import Fraction
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import Tk

preset = 'slower'
crf = '14.5'

def b4ke(video_file,subtitle_file,output_file):
    if os.name=='nt':
        subtitle_file = subtitle_file.replace(':','\\:')
    basename = os.path.basename(video_file)
    if output_file=='':
        output_file = '[BE4K20K]'+basename[:basename.rfind('.')]+'.mp4'
    keyint = int(get_framerate(video_file))*10
    ffmpeg_arg = ['ffmpeg',
                          '-i',str(video_file),
                          '-c:a','aac',
                          '-ar','44100',
                          '-b:a','320k',
                          '-filter_complex','ass=f=\'%s\''%subtitle_file,
                          '-c:v','libx264',
                          '-preset',preset,
                          '-crf', crf,
                          '-x264-params','vbv-maxrate=20000:vbv-bufsize=40000:keyint=%d'%keyint,
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
        video_file = sys.argv[1]
        subtitle_file = sys.argv[2]
        output_file = ''
    else:
        Tk().withdraw()
        video_file = askopenfilename(filetypes=[('MP4 video file','.mp4')],title='Select video file')
        subtitle_file = askopenfilename(filetypes=[('ASS subtitle file','.ass')],title='Select subtitle file')
        vid_base = os.path.basename(video_file)
        output_file = asksaveasfilename(filetypes=[('MP4 video file','.mp4')],title='Select output file',
                                        initialfile='[BE4K20K]'+vid_base[:vid_base.rfind('.')]+'.mp4')
    
    b4ke(video_file,subtitle_file,output_file)

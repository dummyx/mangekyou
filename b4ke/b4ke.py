# -*- coding: UTF-8 -*-
import os
import subprocess
import sys
import shutil
from fractions import Fraction
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import Tk

preset = 'faster'
crf = '18.5'
ha = False

encoder = 'libx264'
#libx264 or h264_amf
bitrate = '23000k'

sound_file = ''

if ha:
    if os.name == 'nt':
        ha_api = 'd3d11va'
    elif os.name == 'posix':
        ha_api = 'vaapi'

x264_params = 'vbv-maxrate={}:vbv-bufsize=40000:keyint={}'
x264_args = ['-preset', preset,
             '-crf', crf,
             '-x264-params']

subtitle_temp = 'b4ke_subtitle_tmp.ass'


def b4ke(video_file, subtitle_file, output_file):
    #if os.name == 'nt':
    #    subtitle_file = subtitle_file.replace(':', '\\:')
    sub_dir = os.path.dirname(subtitle_file)

    shutil.copyfile(subtitle_file, os.path.join(sub_dir, subtitle_temp))
    basename = os.path.basename(video_file)
    if output_file is None:
        output_file = '[BE4K20K]'+basename[:basename.rfind('.')]+'.mp4'
    keyint = int(get_framerate(video_file))*10
    ffmpeg_arg = ['ffmpeg',
                  '-i', str(video_file),
                  '-c:a', 'copy',
                  #'-ar', ' 44100',
                  #'-b:a', '320k',
                  '-filter_complex',
                  'scale=3840:-1:flags=lanczos[sc];[sc]ass=f=\'%s\'' % os.path.join(sub_dir, subtitle_temp).replace('\\','/').replace(':', '\\:'),
                  '-c:v', encoder,
                  output_file]
    if encoder == 'libx264':
        for arg in x264_args:
            ffmpeg_arg.insert(-1, arg)
        ffmpeg_arg.insert(-1, x264_params.format(bitrate, keyint))
    else:
        ffmpeg_arg.insert(-1, '-b:v')
        ffmpeg_arg.insert(-1, bitrate)
    
    print(ffmpeg_arg)

    if ha:
        ffmpeg_arg.insert(1, '-hwaccel')
        ffmpeg_arg.insert(2, ha_api)

    subprocess.run(ffmpeg_arg)
    os.remove(subtitle_temp)


def get_framerate(video_file):
    ffprobe_arg = ['ffprobe',
                   '-v', 'error',
                   '-select_streams', 'v',
                   '-of', 'default=noprint_wrappers=1:nokey=1',
                   '-show_entries', 'stream=r_frame_rate',
                   video_file]
    ffprobe_run = subprocess.run(ffprobe_arg, capture_output=True)
    framerate = float(Fraction(ffprobe_run.stdout.decode()))
    return framerate


if __name__ == '__main__':
    if len(sys.argv) == 3:
        video_file = sys.argv[1]
        subtitle_file = sys.argv[2]
        output_file = None
    else:
        Tk().withdraw()
        video_file = askopenfilename(filetypes=[('MP4 video file', '.mp4')],
                                     title='Select video file')
        subtitle_file = askopenfilename(filetypes=[('ASS subtitle file', '.ass')],
                                        title='Select subtitle file')
        vid_base = os.path.basename(video_file)
        output_file = asksaveasfilename(
                      filetypes=[('MP4 video file', '.mp4')],
                      title='Select output file',
                      initialfile='[BE4K20K]'+vid_base[:vid_base.rfind('.')]+'.mp4')

    b4ke(video_file, subtitle_file, output_file)

    if os.name == 'nt' and sound_file != '':
        import winsound
        winsound.PlaySound(sound_file, winsound.SND_FILENAME)

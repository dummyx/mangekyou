import subprocess
import zipfile
import sys
import os

if __name__ == '__main__':
    p7z_args = ['7za', 'a', '-t7z', '-m0=lzma2', '-mx=9', '-mfb=64', '-md=32m']


    original_file_path = sys.argv[1]
    output_file_path = original_file_path[:original_file_path.rfind('.')]+'.7z'
    
    original_file = zipfile.ZipFile(original_file_path)
    name_list = original_file.namelist()
    for f in name_list:
        original_file.extract(f)
        subprocess.run(p7z_args+[output_file_path,f])
        if not os.path.isdir(f):
            os.remove(f)
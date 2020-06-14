#import subprocess
import zipfile
import tarfile
import sys
import os
import io

if __name__ == '__main__':
    #p7z_args = ['7za', 'a', '-si','-t7z', '-m0=lzma2', '-mx=9', '-mfb=64', '-md=32m']


    original_file_path = sys.argv[1]
    output_file_path = original_file_path[:original_file_path.rfind('.')]+'.tar.xz'
    
    original_file = zipfile.ZipFile(original_file_path)
    info_list = original_file.infolist()
    
    extracted_stream = io.BytesIO()
    tar_stream = io.BytesIO()
    tar = tarfile.open(name=output_file_path,mode='w:xz')
    
    for f in info_list:
        if f.is_dir():
            continue
        extracted_stream.write(original_file.read(f))
        extracted_stream.seek(0)
        info = tarfile.TarInfo(name=f.filename)
        info.size = extracted_stream.getbuffer().nbytes
        tar.addfile(info, extracted_stream)
        extracted_stream.flush()

        #subprocess.run(p7z_args+[output_file_path,f])
        print('Added %s'%f.filename,end='\r')
    tar.close()
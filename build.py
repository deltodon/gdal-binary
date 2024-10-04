import os
import shutil
import subprocess
import sys

def build():
    # Run the standard build process
    subprocess.check_call([sys.executable, '-m', 'build'])

    # Copy GDAL libraries to the package directory
    gdal_lib_dir = os.path.join('build', 'gdal_install')
    target_dir = os.path.join('build', 'lib', 'gdal_binary')
    
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    
    shutil.copytree(gdal_lib_dir, target_dir)

    print("GDAL libraries copied successfully.")

if __name__ == '__main__':
    build()

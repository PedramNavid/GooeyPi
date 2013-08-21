import os
import subprocess
import sys

def pyversion(installdir):
    flags=[]
    flags.append(sys.executable)
    pylocation = os.path.join(installdir, 'pyinstaller.py')
    flags.append(pylocation)
    flags.append('--version')
    p = subprocess.Popen(flags, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out,err = p.communicate()
    return float(out.strip())

    

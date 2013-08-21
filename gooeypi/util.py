import os
import subprocess
import sys
import controller

def pyversion(installdir):
    config = controller.getConfig()
    sys.path.insert(0, installdir)
    from PyInstaller import get_version
    return float(get_version()[:3])

def getflags(fname):
    config = controller.getConfig()
    flags=[]
    flags.append(sys.executable) # Python executable to run pyinstaller
    flags.append(os.path.join(config['pyidir'], 'pyinstaller.py'))
    if config['noconfirm']:
        flags.append('--noconfirm')
    if config['singlefile']:
        flags.append('--onefile')
    if config['ascii']:
        flags.append('--ascii')
    if config['windowed']:
        flags.append('--noconsole')
    if config['upxdir'] != '':
        flags.append('--upx-dir=' + config['upxdir'])
    if pyversion(config['pyidir']) == 2.1:
        flags.append('--distpath=' + os.path.dirname(fname)) # Output to same dir as script.
    else:
        flags.append('--out=' + os.path.dirname(fname))
    flags.append(fname)
    return(flags)
                     
    

    

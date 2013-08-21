'''
Created on Aug 7, 2013

@author: 813365079
'''
import configobj
import os
import sys
from validate import Validator
 
appPath = os.path.abspath(os.path.dirname(os.path.join(sys.argv[0])))
inifile = os.path.join(appPath, "settings.ini")
 
def createConfig():
    """
    Create the configuration file
    """
    config = configobj.ConfigObj(unrepr=True)
    config.filename = inifile
    config['noconfirm'] = False
    config['singlefile'] = False
    config['ascii'] = False
    config['windowed'] = False
    config['upxdir'] = ''
    config['pyidir'] = ''
    config.write()
 
#----------------------------------------------------------------------
def getConfig():
    """
    Open the config file and return a configobj
    """
    if not os.path.exists(inifile):
        open(inifile, 'w').close()
        createConfig()
    config = configobj.ConfigObj(inifile, unrepr=True, configspec='configspec.ini')
    validator = Validator()
    result = config.validate(validator)
    if result == True: 
        return config
    else:
        raise Exception ("Config file is not valid.") 

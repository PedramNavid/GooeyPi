'''
gooeypi.py 
GooeyPi: A Crossplatform Pyinstaller GUI front-end
Copyright (C) 2013 Pedram Navid 
pedram.navid@gmail.com
Comments, issues, requests, and forks welcome: https://github.com/multiphrenic/GooeyPi
Released under GPL v2. See LICENSE file for details.

'''
import wx
import wx.lib.filebrowsebutton as filebrowse
import subprocess
import sys
import logging
import controller
import pref
import os
import util

def init_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='log.txt',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        )
    if not hasattr(sys, 'frozen'):
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s',
            '%H:%M:%S',
        )
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        
def get_config():
    logging.debug("Loading preferences...")
    for key, value in controller.getConfig().items():
        logging.debug("{}: {}".format(key,value))

class GooeyPi(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(GooeyPi, self).__init__(*args, **kwargs)
        self.InitUI()
        self.SetSize((800,350))
        self.SetTitle('GooeyPi - PyInstaller GUI')
        self.Show()
        self.CheckFirstRun()
        
    def InitUI(self):
        logging.debug('Initializing UI')
        self.panel = wx.Panel(self)
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        editMenu = wx.Menu()
        prefs = editMenu.Append(wx.ID_PREFERENCES, '&Preferences...',
                                'Set Preferences')
        menubar.Append(editMenu, '&Edit')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        self.Bind(wx.EVT_MENU, self.OnPreferences, prefs)

        self.fbb = filebrowse.FileBrowseButton(self.panel, -1, size=(350,-1),  labelText='Select Script:',
                    fileMask="Python Source Files (*.py; *.pyw)|*.pyw;*.py", changeCallback = self.fbbCallback)

        self.txtresults = wx.TextCtrl(self.panel, size=(420,200),
                                      style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.btngo = wx.Button(self.panel, label='Go')
        self.btngo.SetDefault()
        self.btngo.Bind(wx.EVT_BUTTON, self.OnSubmit)
        
        self.btnquit = wx.Button(self.panel, label='Quit')
        self.btnquit.Bind(wx.EVT_BUTTON, self.OnQuit)
        
        self.btnoptions = wx.Button(self.panel, label='Options...')
        self.btnoptions.Bind(wx.EVT_BUTTON, self.OnOptions)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(self.fbb, flag=wx.LEFT|wx.ALIGN_CENTRE_VERTICAL, border=5)
        hbox1.Add(self.btnoptions, flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTRE_VERTICAL, border=5)
        hbox3.Add(self.txtresults, 1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=5)
        hbox4.Add(self.btngo, 1, flag=wx.LEFT|wx.RIGHT, border=5)
        hbox4.Add(self.btnquit, 1, flag=wx.LEFT|wx.RIGHT, border=5)

        vbox.Add(hbox1, flag=wx.TOP|wx.BOTTOM, border=5)
        vbox.Add(hbox2, flag=wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT, border=5)
        vbox.Add(hbox3, flag=wx.TOP|wx.BOTTOM|wx.ALIGN_CENTRE|wx.EXPAND, border=5)
        vbox.Add(hbox4, flag=wx.TOP|wx.BOTTOM, border=5)

        self.panel.SetSizer(vbox)

    def fbbCallback(self, e):
        pass

    def CheckFirstRun(self):
        config = controller.getConfig()
        if config['pyidir'] == '':
            dlg = wx.MessageDialog(None, 'Looks like this is your first run of GooeyPi.\n\
    Please select the Pyinstaller directory.', 'First time setup', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.OnPreferences(None)
    
    def OnSubmit(self, e):    
        if self.fbb.GetValue() == '':
            dlg = wx.MessageDialog(None, 'No File Selected! Please select a Python script before proceeding',
                                     'No file selected', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        flags = util.getflags(self.fbb.GetValue())
        logging.debug('calling subprocess {}'.format(flags))
        for line in self.CallInstaller(flags):
            self.txtresults.AppendText(line)
        
    def OnQuit(self, e):
        self.Close()
    
    def OnPreferences(self, e):
        prefdlg = pref.Preferences(None, title='Edit Preferneces')
        prefdlg.ShowModal()
        prefdlg.Destroy()
    
    def OnOptions(self, e):
        self.OnPreferences(e)

    def CallInstaller(self, flags):
        p = subprocess.Popen(flags, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while(True):
            retcode = p.poll()
            line = p.stdout.readline()
            wx.Yield()
            yield line
            if(retcode is not None):
                yield ("Pyinstaller returned return code: {}".format(retcode))
                break
 
if __name__ == '__main__':
    init_logging()
    get_config()
    logging.debug("Logging initialized. Starting application.")
    app = wx.App()
    frame = GooeyPi(None)
    app.MainLoop()
    

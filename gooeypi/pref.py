import wx
import os
import controller
import logging
import wx.lib.filebrowsebutton as filebrowse

class Preferences(wx.Dialog):
    def __init__(self, *args, **kw):
        super(Preferences, self).__init__(*args, **kw)
        self.InitUI()
        self.SetSize((380,290))
        self.SetTitle("Preferences")
        
    def InitUI(self):
        config = controller.getConfig()
        self.panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        grid1 = wx.FlexGridSizer(0,1,0,0)
        
        self.upx = filebrowse.DirBrowseButton(self.panel, -1, size=(350,-1),  labelText='UPX Directory:',
                    changeCallback = self.upxCallback)
        self.upx.SetValue(config['upxdir'])
        self.pyi = filebrowse.DirBrowseButton(self.panel, -1, size=(350, -1), labelText='PyInstaller Directory:',
                                              changeCallback = self.pyiCallback)
        self.pyi.SetValue(config['pyidir'])
        
        box_title = wx.StaticBox(self.panel, -1, "Default Options")
        box = wx.StaticBoxSizer(box_title, wx.VERTICAL)
        
        self.cb_ctrls = []
        self.cbnoconfirm = wx.CheckBox(self.panel, -1, "Remove output directory without confirmation",
                                     style=wx.RB_GROUP)
        self.cbsinglefile = wx.CheckBox(self.panel, -1, "Create a single file deployment")
        self.cbascii = wx.CheckBox(self.panel, -1, "Do not include unicode encoding")
        self.cbwindowed = wx.CheckBox(self.panel, -1, "Do not open the console when program is launched.")
        
        self.cb_ctrls.append(self.cbnoconfirm)
        self.cb_ctrls.append(self.cbsinglefile)
        self.cb_ctrls.append(self.cbascii)
        self.cb_ctrls.append(self.cbwindowed)
        
        self.cbnoconfirm.SetValue(config['noconfirm'])
        self.cbsinglefile.SetValue(config['singlefile'])
        self.cbascii.SetValue(config['ascii'])
        self.cbwindowed.SetValue(config['windowed'])
        
        btnOK = wx.Button(self.panel, wx.ID_OK, 'OK')
        btnCancel = wx.Button(self.panel, wx.ID_CANCEL, 'Cancel')
        btnOK.Bind(wx.EVT_BUTTON, self.OnOK)
        btnCancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        
        vbox.Add(self.pyi, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        vbox.Add(self.upx, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        for cb in self.cb_ctrls:
            grid1.Add(cb,0,wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        box.Add(grid1, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        vbox.Add(box, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        hbox.Add(btnOK, 0, flag=wx.wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        hbox.Add(btnCancel, 0, flag=wx.RIGHT|wx.TOP, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_RIGHT)

        self.panel.SetSizer(vbox)
        
    def OnClose(self, e):
        self.Destroy()

    def OnOK(self, e):
        if self.CheckUPX() and self.CheckPyi():
            config = controller.getConfig()
            config['noconfirm'] = self.cbnoconfirm.GetValue()
            config['singlefile'] = self.cbsinglefile.GetValue()
            config['ascii'] = self.cbascii.GetValue()
            config['windowed'] = self.cbwindowed.GetValue()
            config['upxdir'] = self.upx.GetValue()
            config['pyidir'] = self.pyi.GetValue()
            logging.info("Preferences Saved")
            config.write()
            self.Destroy()

    def OnCancel(self, e):
        self.Destroy()
        
    def upxCallback(self, e):
        pass
    
    def pyiCallback(self, e):
        pass
    
    def CheckUPX(self):
        upxname = ('upx.exe', 'upx')
        # Test if anything in upxname is found in the upx directory provided. 
        if self.upx.GetValue() == '' or [i for i in upxname if i in os.listdir(self.upx.GetValue())] :
            return True
        else:
            dial = wx.MessageDialog(None, 'UPX binary not found. Please check path and try again, or leave blank.',
                                     'Path not found?', 
            wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            dial.Destroy()
            return False
        
    def CheckPyi(self):
        if os.path.exists(os.path.join(self.pyi.GetValue() , 'pyinstaller.py')):
            return True
        else:
            dial = wx.MessageDialog(None, 'pyinstaller.py not found. Please check path.',
                                     'Pyinstaller not found', 
            wx.OK | wx.ICON_ERROR)
            dial.ShowModal()
            dial.Destroy()
            return False

import wx
import switchpanel as sp

class LosePanel(sp.SwitchPanel):
    def init_ui( self, world ):
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText( self, label="YOU ARE KILL" )
        self.sizer.Add( self.text, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)

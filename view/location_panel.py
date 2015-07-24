import wx
import switchpanel as sp

class LocationPanel( sp.SwitchPanel ):
    def init_ui( self, world ):
        self.world = world
        self.info_pane = wx.TextCtrl( self, style=wx.TE_READONLY )
        
    def on_switch( self ):
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        button_sizer = wx.BoxSizer( wx.VERTICAL )
        for name, action, target in self.world.get_location_actions():
            btn = wx.Button( self, label=name )
            def on_push(evt):
                action()
                if target:
                    self.Parent.transition( target )
            button_sizer.Add( btn, 1 )
        sizer.Add( button_sizer, 1, wx.EXPAND )
        self.info_pane.SetValue( self.world.get_location_info() )
        sizer.Add(self.info_pane, 1, wx.EXPAND )

        self.SetSizer( sizer )

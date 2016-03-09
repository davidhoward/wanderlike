import wx
import switchpanel as sp

class LocationPanel( sp.SwitchPanel ):
    def init_ui( self, game ):
        self.game = game
        self.info_pane = wx.TextCtrl( self, style=wx.TE_READONLY )
        
    def on_switch( self ):
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        button_sizer = wx.BoxSizer( wx.VERTICAL )
        for action in self.game.get_location_actions():
            btn = wx.Button( self, label=action.name )
            def on_push(evt):
                self.Parent.transition(action(self.game))
            btn.Bind(wx.EVT_BUTTON, on_push)
            button_sizer.Add( btn, 1 )
        sizer.Add( button_sizer, 1, wx.EXPAND )
        self.info_pane.SetValue( self.game.get_location_info() )
        sizer.Add(self.info_pane, 2, wx.EXPAND )

        self.SetSizer( sizer )

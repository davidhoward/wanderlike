import wx
import src
import view

class MainFrame( wx.Frame ):
    def __init__( self ):
        player = src.player.Player()
        loc = src.location.DungeonTestLocation()
        world = src.world.World( player, use_points=[loc] )
        worl.active_loc = loc
        
        sizer = wx.BoxSize( wx.VERTICAL )
        self.panel = view.DungeonPanel( self, world )
        sizer.Add( self.panel, 1, wx.EXPAND )

        self.SetSizer( sizer )
        self.panel.on_switch()
        self.Bind( wx.EVT_CLOSE, self.OnClose )

    def OnClose( self, evt ):
        self.panel.Freeze()
        self.Destroy()
        
if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()

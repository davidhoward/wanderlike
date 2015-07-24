import wx
import switchpanel as sp
import src


class MapPanel( sp.DrawPanel ):
    def init_ui( self, world ):
        self.world = world
        
    def draw( self, gc ):
        X, Y = self.GetSize()
        d = 5

        brushes = [ wx.Brush("Blue"),
                    wx.Brush("Green"),
                    wx.Brush("Red"),
                    wx.Brush("Yellow"),
                    wx.Brush("Violet"),
                    wx.Brush("Brown") ]

        gc.SetBrush(wx.WHITE_BRUSH)
        gc.DrawRectangle(0,0,X,Y)
        def map_coords(point):
            return int(point.x*X), int(point.y*Y)


        # draw neighbor lines
        for point in self.world.points:
            x, y = map_coords(point)
            gc.SetPen( wx.Pen("Black"))            
            for n in point.neighbors:
                x2, y2 = map_coords(n)
                gc.StrokeLine( x, y, x2, y2 )
            gc.SetPen(wx.Pen("Blue"))
            for t in point.river_targets:
                x2, y2 = map_coords(t)
                gc.StrokeLine( x, y, x2, y2 )
                      
        gc.SetPen(wx.TRANSPARENT_PEN)
        for point in self.world.points:
            x = int(point.x*X)
            y = int(point.y*Y)
            gc.SetBrush( brushes[point.continent_index] )
            gc.DrawEllipse( x-d, y-d, 2*d, 2*d )
            
class MainFrame(wx.Frame):
    def __init__( self, world ):
        wx.Frame.__init__(self, None)
        self.panel = MapPanel( self, world )
        self.sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.sizer.Add( self.panel, 1, wx.EXPAND )

        self.SetSizer( self.sizer )

        self.Bind(wx.EVT_CLOSE, self.OnClose )
        self.panel.Show()

    def OnClose(self, evt):
        self.panel.Freeze()
        self.Destroy()
        
if __name__ == '__main__':
    world = src.world.World( 1000, None )
    app = wx.App(False)
    frame = MainFrame(world)
    frame.Show()
    app.MainLoop()

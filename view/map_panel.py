import wx
import switchpanel as sp

class MapPanel( sp.SwitchPanel ):
    def init_ui( self, world ):
        self.world = world
        self.dx = 0.15
        self.dy = 0.15
        self.draw_origin = self.world.suggest_draw_origin( self.dx, self.dy )
        self.r = 8
        self.font = wx.Font( 11, wx.TELETYPE, wx.NORMAL, wx.BOLD )
        self.movement = self.NO_MOVEMENT
        self.reattach = True
        # bindings
        self.Bind( wx.EVT_LEFT_UP, self.OnClick )
        self.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )
        self.Bind( wx.EVT_KEY_UP, self.OnKeyUp )
        self.Bind( wx.EVT_PAINT, self.OnPaint )
        # create a timer
        self.timer = wx.Timer( self )
        self.Bind( wx.EVT_TIMER, self.OnTick )
        

    def on_post_switch( self ):
        self.timer.Start( 100, False )

    def off_switch( self ):
        self.timer.Stop()

    def OnPaint( self, evt ):
        dc = wx.BufferedPaintDC( self )
        gc = wx.GraphicsContext.Create( dc )
        self.increment_movement()
        #bgbrush = wx.Brush( data.BACKGROUND_COLORS[ self.world.time ] )
        bgbrush = wx.Brush( "#BF9619" )
        gc.SetBrush( bgbrush )
        X, Y = self.GetSize()
        gc.DrawRectangle( 0, 0, X, Y )
        gc.SetFont( self.font )
        pts = self.world.points_within( self.draw_origin, self.dx, self.dy )
        xo = self.draw_origin[0]
        yo = self.draw_origin[1]
        for pt in pts:
            x = int(X*(pt.x-xo)/self.dx)
            y = int(Y*(pt.y-yo)/self.dy)

            gc.SetBrush( wx.Brush( pt.get_color() ) )
            R = self.r*(2)
            gc.DrawEllipse( x-(R/2), y-(R/2), R, R )
            name = pt.get_name()
            tx = max( 0, x-(3*len(name)))
            ty = y + (R/2) - 12
            gc.DrawText( name, tx, ty )
        # draw player
        x_, y_ = self.world.player_coords()
        x = int(X*(x_-self.draw_origin[0])/self.dx)
        y = int(Y*(y_-self.draw_origin[1])/self.dy)
        gc.SetBrush( wx.WHITE_BRUSH )
        gc.DrawEllipse( x-4, y-4, 8, 8 )
        

    NO_MOVEMENT = 0
    MOVE_NORTH = 1
    MOVE_EAST = 2
    MOVE_SOUTH = 4
    MOVE_WEST = 8

    STOP_NORTH = 14
    STOP_EAST = 13
    STOP_SOUTH = 11
    STOP_WEST = 7
    
    def increment_movement( self ):
        
        if self.reattach:
            self.draw_origin = self.world.suggest_draw_origin( self.dx, self.dy )


        mag = 0.005
        if self.movement & self.MOVE_NORTH:
            self.draw_origin[1] = max( 0.0, self.draw_origin[1] - mag )
        if self.movement & self.MOVE_WEST:
            self.draw_origin[0] = max( 0.0, self.draw_origin[0] - mag )
        if self.movement & self.MOVE_SOUTH:
            self.draw_origin[1] = min( 1.0-self.dy, self.draw_origin[1] + mag )
        if self.movement & self.MOVE_EAST:
            self.draw_origin[0] = min( 1.0-self.dx, self.draw_origin[0] + mag )

    #==================
    # Bindings
    #==================
    
    def OnClick( self, evt ):
        x, y  = evt.GetPositionTuple()
        X, Y = self.GetSize()
        rx = self.dx*float(x)/X
        ry = self.dy*float(y)/Y
        rx += self.draw_origin[0]
        ry += self.draw_origin[1]
        pt = self.world.closest_point( rx, ry, self.r*3/max(self.dx,self.dy) )
        if pt != None:
            self.world.set_target_loc( pt )

    def OnKeyDown( self, evt ):
        code = evt.GetKeyCode()

        if code == ord('W'):
            self.movement |= self.MOVE_NORTH
            self.reattach = False
        elif code == ord('A'):
            self.movement |= self.MOVE_WEST
            self.reattach = False
        elif code == ord('S'):
            self.movement |= self.MOVE_SOUTH
            self.reattach = False
        elif code == ord('D'):
            self.movement |= self.MOVE_EAST
            self.reattach = False

    def OnKeyUp( self, evt ):
        code = evt.GetKeyCode()

        if code == ord('W'):
            self.movement &= self.STOP_NORTH
        elif code == ord('A'):
            self.movement &= self.STOP_WEST
        elif code == ord('S'):
            self.movement &= self.STOP_SOUTH
        elif code == ord('D'):
            self.movement &= self.STOP_EAST
        elif code == wx.WXK_SPACE:
            self.reattach = True
        

    def OnTick( self, evt ):
        mode = self.world.tick()
        if mode == "map" or mode is None:
            self.Refresh(eraseBackground=False)
            self.Update()
        else:
            self.Parent.transition( mode )

import wx
import switchpanel as sp

class DungeonMapPanel( sp.DrawPanel ):
    def init_ui( self, world ):
        self.world = world
        self.event_font = wx.Font( 24,
                                   wx.FONTFAMILY_SCRIPT,
                                   wx.FONTSTYLE_NORMAL,
                                   wx.FONTWEIGHT_BOLD )
        
        self.action_font = wx.Font( 14,
                                    wx.FONTFAMILY_DEFAULT,
                                    wx.FONTSTYLE_NORMAL,
                                    wx.FONTWEIGHT_NORMAL )

        self.Bind( wx.EVT_KEY_UP, self.OnKeyPress )
        self.Bind( wx.EVT_LEFT_UP, self.OnClick )
        
    def synchronize( self ):
        self.update_drawing()
        
    def draw( self, gc ):
        dungeon = self.world.get_active_dungeon()
        points = dungeon.get_points()
        X,Y = self.GetSize()

        # draw background
        gc.SetBrush( wx.BLACK_BRUSH )
        gc.DrawRectangle( 0, 0, X, Y )

        RED_PEN = wx.Pen("Red")
        # draw edges
        for point in points:
            px, py = point.x, point.y
            if not point.is_known():
                continue
            
            for n  in point.neighbors:
                if not n.is_known():
                    continue
                nx, ny = n.x, n.y
                if point.path_explored( n ):
                    gc.SetPen( wx.WHITE_PEN )
                else:
                    gc.SetPen( RED_PEN )
                gc.StrokeLine( px*X, py*Y, nx*X, ny*Y )
                
        # draw points
        R = 16
        gc.SetPen( wx.WHITE_PEN )
        RED_BRUSH = wx.Brush("Red")
        for point in points:
            if not point.is_known():
                continue
            
            x = point.x*X
            y = point.y*Y
            if dungeon.is_current_position( point ):
                gc.SetBrush( wx.Brush("yellow") )
                gc.DrawEllipse( x - (R+4)/2, y - (R+4)/2, R+4, R+4 )
                             
            if point.is_visited():
                if point.get_encounter() is not None:
                    gc.SetBrush(wx.RED_BRUSH)
                else:
                    gc.SetBrush(wx.WHITE_BRUSH)
            else:
                gc.SetBrush(wx.BLACK_BRUSH)
            gc.DrawElipse( x - R/2, y - R/2, R, R )
            
        # draw encounter
        encounter = self.world.get_active_encounter()
        if encounter is None:
            return

        gc.SetPen( wx.BLACK_PEN )
        gc.SetTextColor("white")

        gc.SetFont( self.event_font )
        w, h, d, el = gc.GetFullTextExtent( encounter.get_name() )
        gc.DrawText( encounter.get_name(), (X-w)/2, Y/3 - h/2 )

        gc.SetFont( self.action_font )

        info_y = Y/3 + h
        for info in encounter.get_infos():
            w, h, d, el = gc.GetFullTextExtent( info )
            gc.DrawText( info, (X-w)/2, info_y )
            info_y += 5*h/4

        action_y = 2*Y/3
        action_texts = [ action.get_text() for action in encounter.get_actions() ]
        i = 1
        maxi = len(action_texts) + 1
        for atext in action_texts:
            w, h, d, el = gc.GetFullTextExtent( atext )
            action_x = (float(i)/maxi)*X - w/2
            gc.DrawText( atext, action_x, action_y )

    def OnClick( self, evt ):
        if self.world.get_active_encounter() is not None:
            return

        dungeon = self.world.get_active_dungeon()
        X, Y = self.GetSize()
        x, y = evt.GetPosition()
        pt = dungeon.closest_point( float(x)/X, float(y)/Y ):
        if dungeon.can_reach( pt ):
            dungeon.travel_to( pt )
            self.Parent.synchronize()
        
    def OnKeyPress( self, evt ):
        code = evt.GetKeyCode()
        encounter = self.world.get_active_encounter()
        if encounter is None:
            return

        print 'received key press', chr(code)

        if encounter.process_action(chr(code).upper()):
            self.Parent.synchronize()
            
class DungeonPanel( sp.SwitchPanel ):
    def initu_ui( self, world ):
        self.world = world

        self.sizer = wx.BoxSizer( wx.VERTICAL )
        # status bar
        self.status_bar = DungeonStatusBar( self, world )
        self.sizer.Add( self.status_bar, 1 )
        # dungeon map
        self.map_panel = DungeonMapPanel( self, world )
        self.sizer.Add( self.map_panel, 8, wx.EXPAND )
        # action cards
        self.action_deck = DungeonActionDeck( self, world )
        self.action_deck.Add( self.action_deck, 1 )

        self.SetSizer( self.sizer )


    def synchronize( self ):
        self.status_bar.synchronize()
        self.map_panel.synchronize()
        self.action_deck.synchronize()
        

    def switch_on( self ):
        self.world.get_active_dungeon().reset()
        self.synchronize()

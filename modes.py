import itertools
import wx
import switchpanel as sp
import data

def all_modes():
    return ( (tp.mode_name, tp) for tp in ModeRegistrar.registry )

class ModeRegistrar( type ):
    registry = []
    def __init__( cls, name, bases, dict_ ):
        type.__init__( cls, name, bases, dict_ )
        cls.registry.append(cls)


class ActivityMode( sp.SwitchDrawPanel ):
    button_height = .08
    button_border = .01
    button_width = 0.2

    def init_ui( self, world ):
        # state
        self.world = world
        self.buttons = {}

        self.background = wx.Brush( data.BACKGROUND_COLOR )
        self.button_brush = wx.Brush( data.BUTTON_BRUSH_COLOR )
        self.button_pen = wx.Pen( data.BUTTON_PEN_COLOR )
        self.font = wx.Font(  11, wx.TELETYPE, wx.NORMAL, wx.BOLD )
        # bindings
        self.Bind( wx.EVT_LEFT_UP, self.OnClick )
        # special setup
        self.init_mode()

    def init_mode( self ):
        pass


    def add_button( self, name, action ):
        self.buttons[name] = action

    def button_coords( self, X, Y ):
        bby = int(Y*self.button_border)
        bbx = int(X*self.button_border)
        bx = int(X*self.button_width)
        by = int(Y*self.button_height)
        offy = bby
        for button in self.buttons:
            b = ( bbx, offy, bbx+bx, offy+by )
            offy += (by + 2*bby)
            #print 'button ', button, b
            yield b

            
    def draw( self, gc ):
        X, Y = self.GetSize()
        gc.SetBrush( self.background )
        gc.DrawRectangle( 0, 0, X, Y )

        # buttons
        gc.SetFont( self.font )
        gc.SetBrush( self.button_brush )
        gc.SetPen( self.button_pen )
        for button, coord in itertools.izip(self.buttons, self.button_coords(X,Y)):
            x1, y1, x2, y2 = coord
            gc.DrawRectangle( x1, y1, x2-x1, y2-y1 )
            gc.DrawText( button, x1 + int(0.2*(x2-x1)), y1 + int(0.1*(y2-y1)) )

        # status text
        offx = int(0.8*X)
        offy = int(0.1*Y)
        yincr = 15
        for line in self.status_text():
            gc.DrawText( offx, offy, line )
            offy += yincr


    def drop_button( self, name ):
        del self.buttons[name]

    def OnClick( self, evt ):
        x, y = evt.GetPositionTuple()
        #print 'clicked', x, y
        X, Y = self.GetSize()
        all_coords = self.button_coords( X, Y )
        for button, coord in itertools.izip( self.buttons.itervalues(), all_coords ):
            x1, y1, x2, y2 = coord
            if x1 <= x <= x2 and y1 <= y <= y2:
                button()
                return

    # frequently used buttons
    def OnCamp( self ):
        pass

    def OnLeave( self ):
        self.Parent.transition( "map" )

    def OnScavenge( self ):
        scav = self.world.scavenge_active()
        scav_name = self.world.active_loc.get_name() 
        self.world.set_loot( scav, scav_name, show_vals=False )
        self.Parent.transition( "trade" )

    def status_text( self ):
        return []

class EnterTownMode( ActivityMode ):
    __metaclass__ = ModeRegistrar
    mode_name = "enter_town"
    
    def init_mode( self ):
        self.add_button( "Trade", self.OnTrade )
        self.add_button( "Stay", self.OnStay )
        self.add_button( "Leave", self.OnLeave )


    def OnTrade( self ):
        self.Parent.transition( "trade_town" )

    def OnStay( self ):
        pass

class EnterRuinMode( ActivityMode ):
    __metaclass__ = ModeRegistrar
    mode_name = "enter_ruin"
    
    def init_mode( self ):
        self.add_button( "Camp", self.OnCamp )
        self.add_button( "Leave", self.OnLeave )
        self.add_button( "Scavenge", self.OnScavenge )

class EnterWasteMode( ActivityMode ):
    __metaclass__ = ModeRegistrar
    mode_name = "enter_waste"

    def init_mode( self ):
        self.add_button( "Camp", self.OnCamp )
        self.add_button( "Leave", self.OnLeave )
        self.add_button( "Scavenge", self.OnScavenge )

        

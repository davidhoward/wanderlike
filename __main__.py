import argparse
import os
import sys
import wx

import switchpanel as sp

import src
import data
import view

class MainFrame( sp.SwitchFrame ):
    def init_ui( self, world ):
        self.world = world
        self.SetSize( (800, 600) )
        
        self.add_panel( "map", view.MapPanel( self, self.world ) )
        self.add_panel( "location", view.LocationPanel( self, self.world ) )

        self.set_active( "map" )
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_points", help="save point map to file")
    parser.add_argument("--point_map_file", help="load point map from specified file")
    parser.add_argument("--num_points", help="number of location points to generate",
                        type=int, default=1000 )
    args = parser.parse_args()
    
    point_file = os.path.abspath(args.point_map_file) if args.point_map_file else ""
    world = src.world.World( src.player.Player(),
                             generate_points=args.num_points,
                             point_file=point_file )

    if args.save_points:
        world.save_points_to_file( os.path.abspath(args.save_points) )
                                   
    app = wx.App(False)
    frame = MainFrame(world)
    frame.Show()
    app.MainLoop()

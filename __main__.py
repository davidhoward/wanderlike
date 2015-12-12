import argparse
import os
import sys
import wx

import switchpanel as sp

import src
import data
import view

class MainFrame( sp.SwitchFrame ):
    def init_ui( self, game ):
        self.game = game

        
        self.add_panel( src.MAP_MODE, view.MapPanel( self.container, self.game ) )
        self.add_panel( src.LOC_MODE, view.LocationPanel( self.container, self.game ) )
        self.add_panel( src.FIGHT_MODE, view.FightPanel( self.container, self.game ) )
        self.add_panel( src.LOSE_MODE, view.LosePanel( self.container, self.game ) )
        
        self.SetSize( (800, 600) )        
        self.set_active( src.MAP_MODE )
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--point_map_file", help="load point map from specified file")
    parser.add_argument("--num_points", help="number of location points to generate",
                        type=int, default=1000 )
    args = parser.parse_args()
    game = src.engine.Engine( src.world.WorldOpts(args),
                              src.player.PlayerOpts(args),
                              os.path.dirname(__file__) + "/data/root.json")

    app = wx.App(False)
    frame = MainFrame(game)
    frame.Show()
    app.MainLoop()

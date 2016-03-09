import wx
import switchpanel as sp
import wanderlikeview as wlv
class GatherPanel(sp.SwitchPanel):
    def init_ui(self, game):
        self.game = game

    def on_switch(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        log = wlv.LogPane(self)
        buttons = wlv.ButtonPane(self, log=log)
        
        buttons.add_transition("Leave", wlv.LOC_MODE)
        for ract in self.game.get_location_resource_actions():
            buttons.add_action(ract)
        
        sizer.Add(buttons.get_sizer(), 1, wx.EXPAND)
        sizer.Add(log, 2, wx.EXPAND)
        self.SetSizer(sizer)
        

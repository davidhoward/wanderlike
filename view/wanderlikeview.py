import wx
from .. import src.modes.*

class ButtonPane(object):
    def __init__(self, parent, game, log=None, orientation=wx.VERTICAL):
        self.log = log
        self.sizer = wx.BoxSizer(orientation)
        self.parent = parent
        
    def add_transition(self, name, target):
        btn = wx.Button(self.parent, label=name)
        def on_push(evt):
            self.parent.Parent.transition(target)
        btn.Bind(wx.EVT_BUTTON, on_push)
        self.sizer.Add(btn, 1)
        
    def add_action(self, action, game):
        btn = wx.Button(self.parent, action.name)
        def on_push(evt):
            mode, msgs = action(game)
            if self.log:
                self.log.add_message(msg)
            self.paren.Parent.transition(mode)
        btn.Bind(wx.EVT_BUTTON, on_push)
        self.sizer.Add(btn, 1)

    def get_sizer(self):
        return self.sizer


class LogPane(wx.TextCtrl):
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE|wx.TE_READONLY)

    def add_message(self, msgs):
        self.SetValue(self.GetValue() + "\n" + "\n".join(msgs))

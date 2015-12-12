import switchpanel as sp
import wx
import src


class CombatantPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__( self, parent )

        self.sizer = wx.BoxSizer( wx.VERTICAL )
        self.info = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_CENTRE)
        self.sizer.Add(self.info, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
    def update( self, combatant ):
        lines = []
        lines.append(combatant.name)
        for stat in ['strength', 'cunning', 'will']:
            val = getattr(combatant, stat)
            if val > 0:
                lines.append("%s %d" % (stat, val))
        lines.append("health %d/%d" %(combatant.health, combatant.fortitude*10))
        if combatant.last_roll:
            lines.append("")
            lines.append("%s roll: %d" % combatant.last_roll)
            
        self.info.SetValue("\n".join(lines))
        
class FightPanel(sp.SwitchPanel):
    def init_ui( self, game ):
        self.game = game

        self.enemy_panel = CombatantPanel(self)
        self.player_panel = CombatantPanel(self)
        self.fight_button = wx.Button(self, label="Fight")
        self.flee_button = wx.Button(self, label="Flee")

        button_sizer = wx.BoxSizer( wx.HORIZONTAL )
        button_sizer.Add( self.fight_button, 1, wx.EXPAND )
        button_sizer.Add( self.flee_button, 1, wx.EXPAND )
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add( self.enemy_panel, 1, wx.EXPAND )
        self.sizer.Add( self.player_panel, 1, wx.EXPAND )
        self.sizer.Add( button_sizer, 0, wx.EXPAND )
        self.SetSizer(self.sizer)

        self.fight_button.Bind(wx.EVT_BUTTON, self.OnFight)
        self.flee_button.Bind(wx.EVT_BUTTON, self.OnFlee)
        
    def on_switch(self):
        self.fight = self.game.get_fight()
        self.enemy_panel.update(self.fight.get_enemy())
        self.player_panel.update(self.game.get_player())

    def OnFight( self, evt ):
        enemy = self.fight.get_enemy()
        player = self.game.get_player()
        player.fight(enemy, enemy.get_favored_stat())
        self.player_panel.update(player)
        self.enemy_panel.update(enemy)
        if enemy.health <= 0:
            player.add_exp(enemy)
            self.Parent.transition(self.fight.get_parent_mode())
        elif player.health <= 0:
            self.Parent.transition(src.LOSE_MODE)

    def OnFlee( self, evt ):
        enemy = self.fight.get_enemy()
        player = self.game.get_player()
        enemy.attack( player, enemy.get_favored_stat() )
        if player.health <= 0:
            self.Parent.transition(src.LOSE_MODE)
        elif player.test('cunning', enemy.cunning):
            self.Parent.transition(self.fight.get_parent_mode())
    

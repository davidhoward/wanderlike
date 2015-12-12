class Fight(object):
    def __init__( self, enemy, parent_mode):
        self.parent_mode = parent_mode
        self.enemy = enemy
        
    def get_enemy( self ):
        return self.enemy

    def get_parent_mode(self):
        return self.parent_mode


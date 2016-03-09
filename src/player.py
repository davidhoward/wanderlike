import character

class PlayerOpts(object):
    def __init__(self, args):
        pass
    
class Player( character.Character ):
    def __init__( self, opts ):
        # prepare stats

        # initialize
        character.Character.__init__(self, stats)

        # whole map traversal = 6 months
        self.speed = 1.0/(30*6)

    def add_exp(self, enemy):
        pass
    
    def get_status_info(self):
        return []

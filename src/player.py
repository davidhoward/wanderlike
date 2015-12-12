import combatant

class PlayerOpts(object):
    def __init__(self, args):
        pass
    
class Player( combatant.Combatant ):
    def __init__( self, opts ):
        combatant.Combatant.__init__(self)
        self.name = "David"
        # survival
        self.kcal_max = 20 + self.fortitude
        # whole map traversal = 6 months
        self.speed = 1.0/(30*6)

        # skills
        
    def add_exp(self, enemy):
        pass
    

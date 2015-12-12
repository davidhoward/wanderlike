import random

class Combatant(object):
    def __init__(self, stat_pack=None):
        if stat_pack is None:
            self.strength = 1
            self.cunning = 1
            self.will = 1
            self.fortitude = 1
            for i in xrange(6):
                key = random.random()
                if key < 0.25:
                    self.strength += 1
                elif key < 0.5:
                    self.cunning += 1
                elif key < 0.75:
                    self.will += 1
                else:
                    self.fortitude += 1
        else:
            self.strength = stat_pack.get('s', 0)
            self.cunning = stat_pack.get('c', 0)
            self.will = stat_pack.get('w', 0)
            self.fortitude = stat_pack.get('f', 1)

        self.health = self.fortitude*10
        self.last_roll = None

    def get_favored_stat(self):
        stat = '_'
        value = -1
        for s in ['strength', 'cunning', 'will']:
            sval = getattr(self, s)
            if sval > value:
                value = sval
                stat = s
        return stat

    def fight( self, other, stat ):
        sval = self.roll_stat(stat)
        oval = other.roll_stat(stat)
        if sval > oval:
            other.health -= (sval-oval)
        else:
            self.health -= (oval-sval)

    def attack( self, other, stat ):
        sval = self.roll_stat(stat)
        oval = other.roll_stat(stat)
        if sval > oval:
            other.health -= (sval-oval)

    def test( self, stat, target_num ):
        return self.roll_stat(stat) >= target_num

    def roll_stat( self, stat ):
        stat_val = getattr(self, stat, 0)
        roll = 2 + random.randrange(stat_val) + random.randrange(stat_val)
        self.last_roll = (stat, roll)
        return roll

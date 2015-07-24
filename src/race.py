import random

def choose_common_race():
    return random.choice([ HumanRace, OrcRace, TrollRace, DwarfRace, FeyRace, ElfRace ])()

class Race( object ):
    PREF_MILITARY = 0
    PREF_TOWN = 0
    PREF_RELIGION = 0

    def __init__( self ):
        self.pref_military = 1+self.PREF_MILITARY
        self.pref_town = 1+self.PREF_TOWN
        self.pref_religion = 1+self.PREF_RELIGION

        count = 10 - self.pref_military - self.pref_town - self.pref_religion
        for i in xrange(count):
            key = random.random()
            if key < 0.33:
                self.pref_military += 1
            elif key < 0.66:
                self.pref_religion += 1
            else:
                self.pref_town += 1
        
    def suggest_next( self, scores, rank ):
        ts, ms, rs, fc, fp = scores
        ts += 0.01
        ms += 0.01
        rs += 0.01
        ts /= self.pref_town
        ms /= self.pref_military
        rs /= self.pref_religion
        m = min( ts, ms, rs )
        if rank > 1:
            if m == ts:
                return 'TOWN'
            elif m == ms:
                return 'MILITARY'
            elif m == rs:
                return 'RELIGIOUS'
        else:
            if fp < 1.1*fc:
                return 'FARM'
            elif ts < rs:
                return 'MINE'
            else:
                return 'RELIGIOUS'
        
class HumanRace( Race ):
    PREF_TOWN=2

class OrcRace( Race ):
    PREF_TOWN=1
    PREF_MILITARY=1

class TrollRace( Race ):
    PREF_MILITARY=2

class DwarfRace( Race ):
    PREF_MILITARY=1
    PREF_RELIGION=1

class FeyRace( Race ):
    PREF_RELIGION=2

class ElfRace( Race ):
    PREF_RELIGION=1
    PREF_TOWN=1




import random
import location
import race

def random_dominion( rank ):
    if rank == 5:
        return create_dominion( GreaterDominion )
    elif rank == 4:
        return create_dominion( LesserDominion )
    elif rank == 3:
        return create_dominion( PettyDominion )
    else:
        return create_dominion( Wilderness )

def create_dominion( dominion_type ):
    return dominion_type()

class BaseDominion( object ):
    def __init__( self ):
        self.race = self.choose_race()
        self.terrain = self.choose_terrain()
        
        self.capital = None

        self.town_score = 0
        self.military_score = 0
        self.religion_score = 0
        self.food_consumed = 0
        self.food_produced = 0
        
        h = hex(random.randrange(0x1000000))[2:]
        self.color = "#" + "0"*(6-len(h)) + h
        print 'dominion color is ', self.color


    def scores( self ):
        return self.town_score, self.military_score, self.religion_score, self.food_consumed, self.food_produced

    def adjust_scores( self, scores ):
        ts, ms, rs, fc, fp = scores
        self.town_score += ts
        self.military_score += ts
        self.religion_score += ts
        self.food_consumed += fc
        self.food_produced += fp

class GreaterDominion( BaseDominion ):
    def choose_race( self ):
        return race.choose_common_race()
    
    def choose_terrain( self ):
        return location.environ_gen_from_terrain(random.choice(location.GREATER_TERRAIN_TYPES))

    def assign_location( self, pt ):
        if pt.rank == 5:
            self.capital = pt
            loc, scores = location.create_capital( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 4:
            tp = self.race.suggest_next( self.scores(), 4 )
            if tp == 'MILITARY':
                loc, scores = location.create_citadel( self.race, self.terrain )
            else:
                loc, scores = location.create_city( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 3:
            tp = self.race.suggest_next( self.scores(), 3 )
            if tp == 'MILITARY':
                loc, scores = location.create_castle( self.race, self.terrain )
            else:
                loc, scores = location.create_large_town( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 2:
            tp = self.race.suggest_next( self.scores(), 2 )
            if tp == 'TOWN':
                loc, scores = location.create_town( self.race, self.terrain )
            elif tp == 'MILITARY':
                loc, scores = location.create_fort( self.race, self.terrain )
            else:
                loc, scores = location.create_monastery( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 1:
            tp = self.race.suggest_next( self.scores(), 1 )
            if tp == 'FARM':
                loc, scores = location.create_farm_town( self.race, self.terrain )
            elif tp == 'MINE':
                loc, scores = location.create_mine_town( self.race, self.terrain )
            elif tp == 'RELIGIOUS':
                loc, scores = location.create_abbey( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        else:
            loc, scores = location.create_wilderness( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )

class LesserDominion( BaseDominion ):
    def choose_race( self ):
        return race.choose_common_race()

    
    def choose_terrain( self ):
        return location.environ_gen_from_terrain(random.choice(location.LESSER_TERRAIN_TYPES))

    def assign_location( self, pt ):
        if pt.rank == 4:
            self.capital = pt
            loc, scores = location.create_lesser_capital( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 3:
            tp = self.race.suggest_next( self.scores(), 3 )
            if tp == 'MILITARY':
                loc, scores = location.create_castle( self.race, self.terrain )
            else:
                loc, scores = location.create_large_town( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 2:
            tp = self.race.suggest_next( self.scores(), 2 )
            if tp == 'TOWN':
                loc, scores = location.create_town( self.race, self.terrain )
            elif tp == 'MILITARY':
                loc, scores = location.create_fort( self.race, self.terrain )
            else:
                loc, scores = location.create_monastery( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 1:
            tp = self.race.suggest_next( self.scores(), 1 )
            if tp == 'FARM':
                loc, scores = location.create_farm_town( self.race, self.terrain )
            elif tp == 'MINE':
                loc, scores = location.create_mine_town( self.race, self.terrain )
            elif tp == 'RELIGIOUS':
                loc, scores = location.create_abbey( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )

        else:
            loc, scores = location.create_wilderness( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )

class PettyDominion( BaseDominion ):
    def choose_race( self ):
        key = random.random()
        if key < 0.5:
            return race.choose_common_race()
        elif key < 0.8:
            return race.HobRace()
        elif key < 0.9:
            return race.choose_monster_race()
        else:
            return race.VillainRace()

    def choose_terrain( self ):
        return location.environ_gen_from_terrain(random.choice(location.ANY_TERRAIN))


    def assign_location( self, pt ):
        if pt.rank == 3:
            self.capital = pt
            loc, scores = location.create_petty_capital( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 2:
            tp = self.race.suggest_next( self.scores(), 2 )
            if tp == 'TOWN':
                loc, scores = location.create_town( self.race, self.terrain )
            elif tp == 'MILITARY':
                loc, scores = location.create_fort( self.race, self.terrain )
            else:
                loc, scores = location.create_monastery( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )
        elif pt.rank == 1:
            tp = self.race.suggest_next( self.scores(), 1 )
            if tp == 'FARM':
                loc, scores = location.create_farm_town( self.race, self.terrain )
            elif tp == 'MINE':
                loc, scores = location.create_mine_town( self.race, self.terrain )
            elif tp == 'RELIGIOUS':
                loc, scores = location.create_abbey( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )

        else:
            loc, scores = location.create_wilderness( self.race, self.terrain )
            pt.loc = loc
            self.adjust_scores( scores )

class Wilderness( BaseDominion ):

    def choose_terrain( self ):
        return location.eniron_gen_from_terrain(random.choice(location.ANY_TERRAIN))

    def choose_race( self ):
        key = random.random()
        if key < 0.1:
            return race.choose_common_race()
        elif key < 0.2:
            return race.HobRace()
        elif key < 0.5:
            return race.EmptyRace()
        elif key < 0.75:
            return race.choose_monster_race()
        else:
            return race.VillainRace()


    def assign_location( self, pt ):
        if pt.rank == 2:
            loc, scores = loction.create_wilderness_town( self.race, self.terrain )
            pt.loc = loc
        elif pt.rank == 1:
            loc, scores = location.create_wilderness_vilage( self.race, self.terrain )
            pt.loc = loc
        else:
            loc, scores = location.create_wilderness( self.race, self.terrain )
            pt.loc = loc


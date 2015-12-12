import random
import resource
import itemlib
import goods
import modes

#===============================================================================
# Free Functions
#===============================================================================

def normalize( dist ):
    total = sum(dist.itervalues())
    return { k:v/total for k,v in dist.iteritems() }

#===============================================================================
# Classes
#===============================================================================
MAX_POI = 20
class Location(object):
    def __init__( self ):
        self.items = itemlib.Inventory()
        self.resources = []
        self.visited = False
        self.stead = None
        self.town = None
        self.dungeon = None
        self.poi = random.randrange(5,MAX_POI+1)
        
    def get_actions(self, player):
        # name, action -> target_mode
        ret = []
        def make_trans(act):
            def trans(game):
                return act
            return trans
        
        if self.poi > 0:
            ret.append(("Explore", self.expore_action, modes.LOC_MODE))
        camp = True
        if self.town:
            camp = False
            ret.append(("Town", make_trans(modes.TOWN_MODE)))
        if self.stead:
            camp = False
            ret.append(("Home", make_trans(modes.STEAD_MODE)))
        ret.append(("Hunt", make_trans(modes.HUNT_MODE)))
        ret.append(("Leave", make_trans(modes.MAP_MODE)))
        ret.append(("Gather", make_mode(modes.GATHER_MODE)))
        return ret
    
    def get_color( self ):
        if self.visited:
            return "#333333"
        else:
            return "#999999"

    def mode_request(self, player):
        return modes.LOC_MODE


    # resources and caches
    def add_cache(self, game):
        name, num = random.choice(self.bonus_resouces).gen()
        self.items.add(game.get_items(name, num))
        self.add_message("You stumble across %d %s" % (num, name))

    def add_resource(self, game):
        spec = random.choice(self.resources)
        self.resources.add_spec(spec)
        self.add_message("You find a %s, a good source of %s!")
        
    # actions
    def explore_action(self, game):
        # search town if none
        # search dungeon if none
        bonus_chance = float(self.poi)/MAX_POI
        # resource?
        if random.random() < bonus_chance:
            self.add_resource()
            return modes.LOC_MODE
        # random encounter?
        if random.random() < self.danger():
            game.set_fight_with_tags(or_tags=self.env_tags)
            return modes.FIGHT_MODE
        # cache?
        if random.random() < bonus_chance:
            self.add_cache(game)
        # nothing
        else:
            self.add_message("You don't find anything")
        return self.LOC_MODE

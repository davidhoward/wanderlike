import random
import resource
import itemlib
import goods
import modes
import stead
from action import Action

#===============================================================================
# Constants
#===============================================================================
HEIGHT_NONE = -1
HEIGHT_OCEAN = 0
HEIGHT_FLAT = 1
HEIGHT_HILL = 2
HEIGHT_MOUNTAIN = 3

WATER_NONE = -1
WATER_DRY = 0.0
WATER_MODERATTE = 0.25
WATER_WET = 0.5

TEMP_NONE = -1
TEMP_COLD = 0
TEMP_TEMPERATE = 1
TEMP_HOT = 2

THRESH_HOT = 0.34/2
THRESH_TEMPERATE = 0.67/2

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
        self.stead = stead.Stead()
        self.town = None
        self.dungeon = None
        self.poi = random.randrange(5,MAX_POI+1)
        self.terrain = Terrain()
        
    def get_actions(self, player):
        ret = []
        if self.poi > 0:
            ret.append(Action("Explore", modes.LOC_MODE, self.explore_action))
        if self.town:
            ret.append(Action("Town", modes.TOWN_MODE))
        ret.append(Action("Camp" if self.stead.is_camp() else "Home", modes.HOME_MODE))
        ret.append(Action("Hunt", modes.HUNT_MODE))
        ret.append(Action("Leave", modes.MAP_MODE))
        if len(self.resources) > 0:
            ret.append(Action("Gather", modes.GATHER_MODE))
        return ret

    def get_resource_actions(self):
        return [ rsc.harvest_action() for rsc in self.resources ]

    def get_color( self ):
        if self.visited:
            return "#333333"
        else:
            return "#999999"

    def is_mountain(self):
        return self.terrain.height == HEIGHT_MOUNTAIN
    def mode_request(self, player):
        return modes.LOC_MODE


    # resources and caches
    def add_cache(self, game):
        name, num = random.choice(self.bonus_resouces).gen()
        self.items.add(game.get_items(name, num))
        self.add_message("You stumble across %d %s" % (num, name))

    def add_resource(self, game):
        spec = random.choice(game.resources)
        self.resources.append(resource.from_spec(spec))
        self.add_message("You find a %s, a good source of %s!")

    def finish(self, river):
        forest = random.random() < self.terrain.water
        self.name = self.terrain.build_name(forest)
        if forest:
            self.resources.add_spec

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


class LandProbs(object):
    def __init__(self):
        self.hill_chance = 0.0
        self.water = 0.0
        self.n = 0

    def accumulate(self, location):
        t = location.terrain
        if t.height == HEIGHT_NONE:
            return
        elif t.height == HEIGHT_MOUNTAIN:
            self.hill_chance += 0.8
        elif t.height == HEIGHT_HILL:
            self.hill_chance += 0.5
        else:
            self.hill_chance += 0.25

        self.water += t.water
        self.n += 1


    def assign_terrain(self, terrain):
        hill_chance = self.hill_chance/self.n
        if random.random() < hill_chance:
            terrain.height = HEIGHT_HILL

        terrain.water = self.water/n
        
            
class Terrain(object):
    def __init__(self):
        self.height = HEIGHT_NONE
        self.water = WATER_NONE
        self.temp = TEMP_NONE
    

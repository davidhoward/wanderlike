import random
import resource
import itemlib
import goods

#===============================================================================
# Free Functions
#===============================================================================

def normalize( dist ):
    total = sum(dist.itervalues())
    return { k:v/total for k,v in dist.iteritems() }

#===============================================================================
# Classes
#===============================================================================

class LandProbs(object):
    def __init__( self, water_in ):
        raw_probs = { DesertLocation:0.4,
                      PlainsLocation:0.4+0.5*water_in,
                      ForestLocation:0.25+0.5*water_in,
                      MarshLocation:0.0+0.1*water_in,
                      HillsLocation:0.1 }

        self.probs = normalize( raw_probs )

    def accumulate( self, loc ):
        if loc is None:
            return
        prefs = loc.get_land_neighbor_prefs()
        for pref, prob in prefs.iteritems():
            if pref in self.probs:
                self.probs[pref] += prob
            else:
                self.probs[pref] = prob


    def choose_location( self ):
        final_probs = normalize( self.probs )

        running_total = 0.0
        table = []
        for k, v in final_probs.iteritems():
            running_total += v
            table.append( (running_total, k) )

        key = random.random()
        for choice in table:
            if key < choice[0]:
                return choice[1]()
        else:
            return table[-1][1]()

        
class Location(object):
    def __init__( self ):
        self.items = itemlib.Inventory()
        self.resources = []
        self.scouted = False

    def add_items( self, items ):
        for item in items:
            self.add_item( item, random.random() )

    def add_item( self, item, hide ):
        self.items.add_item( item, hidden=hide )

    def add_resource( self, resource ):
        self.resources.append(resource)


    def get_color( self ):
        if self.scouted:
            return "#333333"
        else:
            return "#999999"

    def scavenge( self, player ):
        self.items.set_vis_limit( player.perception )
        return self.items
        


# Location implementation classes. Keep in alphabetical order.
class DesertLocation(Location):
    name = "Desert"

    def get_land_neighbor_prefs( self ):
        return { DesertLocation:0.5, PlainsLocation:0.4,
                 OasisLocation:0.1 }
    
class ForestLocation(Location):
    name = "Forest"

    def get_land_neighbor_prefs( self ):
        return { ForestLocation:0.4, PlainsLocation:0.5,
                 MarshLocation:0.1 }
    
class HillsLocation(Location):
    name = "Hills"

    def get_land_neighbor_prefs( self ):
        return { HillsLocation:0.34,
                 ForestLocation:0.33,
                 PlainsLocation:0.33}

class MarshLocation(Location):
    name = "Marsh"

    def get_land_neighbor_prefs( self ):
        return { MarshLocation:0.5,
                 ForestLocation:0.5 }
    
class MountainLocation(Location):
    name = "Mountain"

    def get_land_neighbor_prefs( self ):
        return { HillsLocation:0.5, PlainsLocation:0.25,
                 ForestLocation:0.25 }

class OasisLocation(Location):
    name = "Oasis"

    def get_land_neighbor_prefs( self ):
        return { DesertLocation:1.0 }

class OceanLocation(Location):
    name = "Ocean"
    def get_land_neighbor_prefs(self):
        return { PlainsLocation:0.5, ForestLocation:0.5 }
        
class PlainsLocation(Location):
    name = "Plains"

    def get_land_neighbor_prefs( self ):
        return { PlainsLocation:0.4,
                 HillsLocation:0.1,
                 ForestLocation:0.25,
                 DesertLocation:0.25 }

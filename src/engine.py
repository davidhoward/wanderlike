import json
import random
import os

import combatant
import fight
import modes
import player
import world

class Bestiary(object):
    def __init__(self):
        self.specs = {}
        self.tag_lists = {}

    def add(self, spec):
        self.specs[spec['name']] = spec
        for tag in spec.get('tags',[]):
            if tag in self.tag_lists:
                self.tag_lists[tag].append(spec)
            else:
                self.tag_lists[tag] = [spec]

    def from_spec(self, spec):
        c = combatant.Combatant( spec )
        c.name = spec['name']
        return c
    
    def random(self):
        spec_name = random.sample(self.specs,1)[0]
        return self.from_spec(self.specs[spec_name])
    
class Engine(object):
    def __init__(self, world_opts, player_opts, data_root):
        self.world = world.World(world_opts)
        self.player = player.Player(player_opts)

        self.load_data(data_root)

        self.time = 8

    #=======================================================
    # game data
    #=======================================================
    def get_fight(self):
        return self.fight

    def get_player(self):
        return self.player
    
    def load_data(self, data_root):
        rootf = open(data_root, 'r')
        data = json.load(rootf)
        rootf.close()
        root_path = os.path.dirname(data_root)
        # load enemies
        self.bestiary = Bestiary()
        for ef_name in data['enemies']:
            ef = open(os.path.join(root_path, ef_name),'r')
            edata = json.load(ef)
            ef.close()
            for spec in edata['specs']:
                self.bestiary.add(spec)

    #=========================================================
    # operations
    #=========================================================
    def map_tick( self ):
        if self.world.target_pos is not None:
            self.time = ( self.time + 1 ) % 24
            new_loc = self.world.increment_travel(self.player)
            if new_loc is None:
                return modes.MAP_MODE
            else:
                #new_loc.arrival( self.player )
                #return new_loc.mode_request( self.player )
                self.fight = fight.Fight(self.bestiary.random(),
                                         parent_mode=modes.MAP_MODE)
                return modes.FIGHT_MODE
        else:
            return None
        
        

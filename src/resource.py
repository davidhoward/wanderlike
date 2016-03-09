import random
import action
import itemlib

class Resource(object):
    def __init__(self):
        pass

    def harvest_action(self):
        return action.Action(self.gather_desc,
                             modes.GATHER_MODE,
                             self.harvest)
    

class ForestResource(Resource):
    gather_desc = "Forest - Chop Wood"
    def harvest(self, game):
        player = game.get_player()
        loc = game.get_location()
        axe = player.inventory.get_item(itemlib.WOOD_AXE)
        if axe is None:
            n = random.randrange(2)
            loc.items.add(itemlib.WOOD, n)
            info = ["Without a wood axe, you gathered %d wood. (%d total)" % (n, loc.items.count(itemlib.WOOD))]
        else:
            n, msg = axe.roll_gather(item.lib.WOOD)
            info = ["You gathered %d wood. (%d total)" % (n, loc.items.count(itemlib.WOOD))]
            if msg:
                info.append(msg)
        return modes.GATHER_MODE, info
            

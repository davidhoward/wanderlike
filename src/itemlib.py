import goods
import random

items_by_type = {}

#===============================================================================
# Free Functions
#===============================================================================

def generate( good_type, a ):
    types = good_type.all_subs()
    amount = a
    possible = []
    for tp in types:
        possible.extend( get_item_type(tp) )
    possible.sort( key=lambda i: i.base_value )
    
    ret = []
    maxi = len(possible)
    while maxi > 0 and amount > 0:
        idx = random.randrange(maxi)
        item_class = possible[idx]
        if item_class.base_value > a:
            maxi = idx-1
        else:
            ret.append( item_class() )
            amount -= item_class.base_value
    return ret

__all__ = [ generate ]

def get_item_type( good_type ):
    global items_by_type
    if good_type in items_by_type:
        return items_by_type[good_type]
    else:
        ret = []
        items_by_type[good_type] = ret
        return ret


#===============================================================================
# Classes
#===============================================================================

class MetaItem( type ):
    def __init__( cls, name, bases, dict_ ):
        type.__init__( cls, name, bases, dict_ )
        for tp in cls.good_types:
            get_item_type(tp).append( cls )

class BaseItem( object ):
    pass

# item class from good
def icfg( good, name, base_value ):
    dict_ = {}
    dict_['base_value'] = base_value
    dict_['name'] = good.name
    dict_['good_types'] = [ good ]
    return MetaItem( name, (BaseItem,), dict_ )

class ChowItem( BaseItem ):
    __metaclass__ = MetaItem
    base_value = 1
    weight = 0.25
    name = "Preserved Chow"
    good_types = [ goods.CHOW ]

class CleanWaterItem( BaseItem ):
    __metaclass__ = MetaItem
    base_value = 2
    weight = 1
    name = "Clean Water"
    good_types = [ goods.CLEAN_WATER ]

class RadWaterItem( BaseItem ):
    __metaclass__ = MetaItem
    base_value = 0.5
    weight = 1
    name = "Radioactive Water"
    good_types = [goods.RAD_WATER]


#===============================================================================
# Inventories
#===============================================================================
class InvData( object ):
    def __init__( self, **kargs ):
        self.qty = 0
        self.hidden = 0.0

class Inventory( object ):
    def __init__( self ):
        self.contents = []

    def add_item( self, item, **kargs ):
        self.contents.append( (item, InvData(**kargs)) )

    def take_item( self, item ):
        self.contents.remove(item)


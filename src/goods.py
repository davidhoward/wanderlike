# global good types
class Good( object ):
    def __init__( self, name, *subs ):
        self.name = name
        self.subs = subs

    def satisfies( self, good ):
        if self is good:
            return True
        else:
            for sub in self.subs:
                if sub.satisfies( good ):
                    return True
            else:
                return False

    def all_subs( self ):
        if len(self.subs) == 0:
            return [self]
        else:
            return reduce( list.__add__, map( lambda sub: sub.all_subs(), self.subs ) )

# foods
HEIRLOOM_VEGETABLES = Good("Heirloom Vegetables")
CLONED_VEGETABLES = Good("Cloned Vegetables")
MUTANT_VEGETABLES = Good("Mutant Vegetables")


VEGETABLES = Good( "Vegetables", HEIRLOOM_VEGETABLES, CLONED_VEGETABLES, MUTANT_VEGETABLES )

HEIRLOOM_FRUITS = Good("Heirloom Fruits")
CLONED_FRUITS = Good("Cloned Fruits")
MUTANT_FRUITS = Good("Mutant Fruits")

FRUITS = Good( "Fruits", HEIRLOOM_FRUITS, CLONED_FRUITS, MUTANT_FRUITS )

WILD_GAME = Good( "Wild Game" )
CLONED_MEAT = Good( "Cloned Meat" )
JERKY = Good( "Jerky" )

MEAT = Good( "Meat", WILD_GAME, CLONED_MEAT, JERKY )

CHOW = Good( "Preserved Chow" )

FOOD = Good( "Food", MEAT, CHOW, FRUITS, VEGETABLES )

CLEAN_WATER = Good( "Clean Water" )
DIRTY_WATER = Good( "Dirty Water" )
RAD_WATER = Good( "Irradiated Water" )

WATER = Good( "Water", CLEAN_WATER, DIRTY_WATER, RAD_WATER )

OLD_FOOD = Good( "Old Food", CHOW, WATER, CLONED_FRUITS, CLONED_VEGETABLES )
WILD_FOOD = Good( "Wild Food", WATER, MUTANT_FRUITS, MUTANT_VEGETABLES )

# materials
mats = []
def add_mat( name ):
    global mats
    mat = Good(name)
    mats.append(mat)
    return mat

STONES = add_mat("Stones")
CONCRETE = add_mat("Concrete Blocks")
MUD_BRICKS = add_mat("Mud Bricks")
WOOD = add_mat("Wood")
SHEET_METAL = add_mat("Corrugated Aluminum")

CONSTRUCTION = Good("Construction Materials", STONES, CONCRETE, MUD_BRICKS, WOOD, SHEET_METAL )

WIRING = add_mat("Wiring")
SEMICONDUCTORS = add_mat("Semiconductors")
IC = add_mat("Integracted Circuits")
MAGNETS = add_mat("Magnets")
CERAMICS = add_mat("Ceramics")
PLASTICS = add_mat("Plastics")
MACHINER = add_mat("Machinery")
PRES_MACH = add_mat("Precision Machinery")
OPTICS = add_mat("Optical Components")

HOUSEDHOLD_CHEM = add_mat("Household Chemicals")
INDUSTRIAL_CHEM = add_mat("Industrial Chemicals")
VOLATILE_CHEM = add_mat("Volatile Chemicals")

MATERIALS = Good( "Materials", *mats )

# arms
PRIMITVE_ARMS = Good("Primitive Arms")
WASTER_ARMS = Good("Waster Arms")
ANCIENT_ARMS = Good("Ancient Arms")
TAC_ARMS = Good("Tactical Arms")
OPTICAL_ARMS = Good("Optical Arms")
PARTICLE_ARMS = Good("Particle Arms")
TECH_ARMS = Good("Tech Arms")

ARMS = Good("Arms", PRIMITVE_ARMS, WASTER_ARMS, ANCIENT_ARMS, TAC_ARMS, OPTICAL_ARMS, 
            PARTICLE_ARMS, TECH_ARMS )

# meds
MEDS = Good("Medicine")

import random
RAD = 0

resource_classes = []

def get_resource_class( idx ):
    global resource_classes
    while len(resource_classes) <= idx:
        resource_classes.append([])
    return resource_classes[idx]


def insert_resource( idx, rsc ):
    cls = get_resource_class(idx)
    
    i = 0
    while i < len(cls) and rsc.min_degree > cls[i].min_degree:
        i += 1
    cls.insert( i, rsc )

def generate( idx, degree ):
    cls = get_resource_class(idx)
    
    minidx = 0
    maxidx = len(cls)
    while minidx < maxidx:
        idx = random.randrange(minidx, maxidx)
        rsc_class = cls[idx]
        if rsc_class.min_degree <= degree <= rsc_class.max_degree:
            return rsc_class(degree)
        elif rsc_class.min_degree > degree:
            minidx = idx
        else:
            maxidx = idx
    else:
        return BogusResource( idx, degree )


class BaseResource( object ):
    pass


class BogusResource( BaseResource ):
    name = "Bogus Resource"
    def __init__( self, idx, degree ):
        self.idx = idx
        self.degree = degree

class RadioactivePoolResource( BaseResource ):
    name = "Radioactive Pool"
    min_degree = 0
    max_degree = 250
    def __init__( self, degree ):
        self.rads = degree
        

class WasteDumpResource( BaseResource ):
    name = "Radioactive Waste Dump"
    min_degree = 200
    max_degree = 1000
    def __init__( self, degree ):
        self.rads = degree


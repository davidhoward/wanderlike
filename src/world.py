import itertools
import math
import pickle
import random

import pointgraph
import blocktree

import location


def area( r ):
    return math.pi*r*r

def radius_from_area( A ):
    return math.sqrt( A / math.pi )

class LocationPoint( pointgraph.Point ):
    #=================
    # Initialization
    #=================    
    def __init__( self, pid, x, y ):
        pointgraph.Point.__init__( self, pid, x, y )
        
        self.loc = None
        self.is_land = True
        self.sea_hops = -1
        self.continent_index = 0
        self.add_ref( "river_targets", set() )
        self.water_in = 0

    def find_sea_hops( self, seen = None):
        if not self.is_land:
            self.sea_hops = 0
            return 0
        elif self.sea_hops > 0:
            return self.sea_hops
        elif seen and self in seen:
            return float('inf')
        else:
            s = seen if seen else set()
            s.add(self)
            self.sea_hops = 1 + reduce( min, [ n.find_sea_hops(s) for n in self.neighbors ] )
            return self.sea_hops
        
    def assign_ocean( self ):
        self.loc = location.OceanLocation()

    def assign_mountain( self ):
        self.loc = location.MountainLocation()

            
    def decide_terrain_land( self ):
        probs = location.LandProbs(self.water_in)
        for n in self.neighbors:
            probs.accumulate( n.loc )

        self.loc = probs.choose_location()

    def push_rivers( self ):
        self.water_in += 1
        
        if self.sea_hops <= 1:
            return

        min_hops = reduce( min, [ n.sea_hops for n in self.neighbors ] )
        if self.sea_hops == min_hops:
            return # probably shouldn't get here.
        
        for n in self.neighbors:
            if n.sea_hops == min_hops:
                self.river_targets.add(n)
                n.push_rivers()
    #=================
    # Operation
    #=================    
    def arrival( self, party ):
        if party.is_player:
            self.loc.scouted = True

    def get_color( self ):
        return self.loc.get_color()

    def get_name( self ):
        if self.loc.scouted:
            return self.loc.name
        else:
            return ""

    def mode_request( self, player ):
        return self.loc.mode_request( player )

    def scavenge( self, player ):
        return self.loc.scavenge( player )

    def river_depth( self ):
        if len(self.river_targets) == 0:
            return 0
        else:
            return 1 + reduce( max, ( t.river_depth() for t in self.river_targets ) )

continent_index = 0
class Continent( pointgraph.PointCluster ):
    """ Used in terrain assignment """
    def __init__( self, start_points, unmarked ):
        pointgraph.PointCluster.__init__( self, start_points, unmarked )

    def assign_sea( self ):
        for point in self.points:
            point.continent_index = 0
            point.is_land = False
            point.assign_ocean()
            
    def assign_land( self ):
        global continent_index
        continent_index += 1
        self.continent_index = continent_index
        for point in self.points:
            point.continent_index = self.continent_index
        
        # place mountains
        num_mountains = max( 5, len(self.points) // 20 )
        if num_mountains > len(self.points):
            num_mountains = 1

        mountain_points = random.sample(self.points, num_mountains)
        for point in mountain_points:
            point.assign_mountain()

        # push rivers
        for point in mountain_points:
            point.push_rivers()

        # assign rest based on neighbors
        for point in self.points:
            point.decide_terrain_land()

class PointDistribution( object ):
    def __init__( self, candidate_size ):
        self.extant = []
        self.candidate_size = candidate_size
        
    def draw_point( self ):
        candidates = [ [ (random.random(), random.random()), 1.0 ] for i in xrange(self.candidate_size) ]
        for x,y in self.extant:
            for candidate in candidates:
                xc, yc = candidate[0]
                dist = (xc-x)**2 + (yc-y)**2
                candidate[1] = min( candidate[1], dist )

        max_dist = -1
        max_coord = (0.5,0.5)
        for coords, dist in candidates:
            if dist > max_dist:
                max_coord = coords
                max_dist = dist
        self.extant.append(max_coord)
        return max_coord
        
class World( object ):
    def __init__( self, player, generate_points=0, use_points=None, point_file="" ):
        if use_points:
            self.points=use_points
        elif point_file:
            self.load_points(point_file)
            self.assign_locations()            
        elif generate_points:
            self.generate_points( npoints )
            self.assign_locations()            
        else:
            raise ValueError("No point set specified for world!")
        


        self.player = player
        self.player_pos = [ random.random(), random.random() ]
        self.target_pos = None
        self.active_loc = None

        self.time = 8

    #=================
    # Initialization
    #=================
    def generate_points( self, npoints ):

        distro = PointDistribution(10)
        def create_point( pid ):
            x, y = distro.draw_point()
            return LocationPoint( pid, x, y )

        self.points = pointgraph.create_points( npoints, create_point )
        
        # build neighborhood graph
        print 'building neighbor candidate lists'
        cutoff = 0.0
        for point in self.points:
            point.build_neighbor_candidate_list( self.points )
            cutoff = max( cutoff, point.dist(point.neighbor_candidates[0]) )
            
        cutoff *= 3
        print 'cutoff', cutoff

        pointgraph.choose_neighbors( self.points, cutoff, True )
        

    def assign_locations( self ):
        # assign continents
        num_continents = 5
        num_seas = 7
        
        print 'assigning continents...'
        continents, oceans, unassigned = pointgraph.assign_clusters( self.points,
                                                                     (Continent, num_continents),
                                                                     (Continent, num_seas ) )

            
        # assign terrain
        for ocean in oceans:
            ocean.assign_sea()

        for point in unassigned:
            point.assign_ocean()
            point.is_land = False
            point.continent_index = 0
            
        for point in self.points:
            point.find_sea_hops()
            
        for continent in continents:
            continent.assign_land()

        print "max tree depth", self.points.max_depth()
        max_river = 0
        for point in self.points:
            max_river = max(max_river, point.river_depth())

        print "max river depth", max_river


    #=================
    # File IO
    #=================
    def load_points( self, point_file_name ):
        self.points = pointgraph.unpickle_points(point_file_name)

    def save_points_to_file( self, point_file_name ):
        ffile = open(point_file_name, 'wb+')
        point_list = list(self.points)
        pickle.dump(list(self.points), ffile)
        ffile.close()
    
    #=================
    # Operation
    #=================

    def closest_point( self, x, y, r ):
        pts = self.points.within( x, y, r )
        if len(pts) == 0:
            return None
        else:
            return pts[0]

    def get_active_loc( self ):
        return self.active_loc

    def get_location_actions( self ):
        return self.active_loc.loc.get_actions( self.player )
    
    def increment_travel( self ):
        tx, ty = self.target_pos
        px, py = self.player_pos
        s = self.player.speed
        a = ty - py
        o = tx - px
        h = math.hypot( a, o )
        if h < s:
            self.player_pos = self.target_pos
            self.active_loc = self.points[ self.target_pos ]
            self.target_pos = None
            return self.points[ self.player_pos ]
        else:
            dx = s/h*o
            dy = s/h*a
            self.player_pos[0] += dx
            self.player_pos[1] += dy
            return None

    def player_coords( self ):
        return self.player_pos

    def points_within( self, c, dx, dy  ):
        x, y = c
        return self.points.within_box( x, y, dx, dy )

    def set_target_loc( self, loc ):
        self.target_pos = [ loc.x, loc.y ]

    def suggest_draw_origin( self, dx, dy ):
        x = max( 0.0, min( 1.0-dx, self.player_pos[0]-(dx/2) ) )
        y = max( 0.0, min( 1.0-dy, self.player_pos[1]-(dy/2) ) )
        return [ x, y ]


    def tick( self ):
        if self.target_pos is not None:
            self.time = ( self.time + 1 ) % 24
            new_loc = self.increment_travel()
            if new_loc is None:
                return "map"
            else:
                new_loc.arrival( self.player )
                return new_loc.mode_request( self.player )
        
        

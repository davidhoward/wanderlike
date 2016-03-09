import itertools
import math
import pickle
import random

import pointgraph
import blocktree

import fight
import location
import modes

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
        
        self.loc = location.Location()
        self.is_land = True
        self.sea_hops = -1
        self.continent_index = 0
        self.add_ref( "river_targets", set() )
        self.river_in = False

    def __repr__(self):
        return "<LocationPoint x=%f y=%f>" % (self.x, self.y)
    
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
        self.loc.terrain.height = location.HEIGHT_OCEAN
        self.loc.terrain.water = 1.0
        
    def assign_mountain( self, water ):
        self.loc.terrain.height = location.HEIGHT_MOUNTAIN
        self.loc.terrain.water = water
            
    def decide_terrain_land( self ):
        probs = location.LandProbs()
        for n in self.neighbors:
            probs.accumulate( n.loc )

        probs.assign_terrain(self.loc.terrain)

    def finish_land(self):
        self.loc.finish( self.river_in )
        
    def is_mountain(self):
        return self.loc.terrain.height == location.HEIGHT_MOUNTAIN
    
    def push_rivers( self ):
        self.river_in = True
        self.loc.terrain.water += 0.1
        
        if self.sea_hops <= 1:
            return

        min_hops = reduce( min, [ n.sea_hops for n in self.neighbors ] )
        if self.sea_hops == min_hops:
            return # probably shouldn't get here.
        
        for n in self.neighbors:
            if n.sea_hops == min_hops:
                self.river_targets.add(n)
                n.push_rivers()

    def set_temp(self):
        lat = abs(self.y - 0.5)
        if lat < location.THRESH_HOT:
            self.loc.terrain.temp = location.TEMP_HOT
        elif lat < location.THRESH_TEMPERATE:
            self.loc.terrain.temp = location.TEMP_TEMPERATE
        else:
            self.loc.terrain.temp = location.TEMP_COLD
    #=================
    # Operation
    #=================    
    def arrival( self, party ):
        if party.is_player:
            self.loc.scouted = True

    def get_color( self ):
        return self.loc.get_color()

    def get_name( self ):
        if self.loc.visited:
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

        non_mountains = set(self.points)
        mountain_points = set()
        while num_mountains > 0  and len(non_mountains) > 0:
            range_size =  1 if num_mountains == 1 else random.randrange(1,num_mountains)
            candidates = set(random.sample(non_mountains,1))
            while range_size > 0:
                m = random.sample(candidates,1)[0]
                m.assign_mountain(0)
                mountain_points.add(m)
                
                non_mountains.remove(m)
                candidates.remove(m)
                
                for p in m.neighbors:
                    if p in non_mountains:
                        candidates.add(p)
                range_size -= 1
                num_mountains -= 1

        # assign rest based on neighbors
        candidates = list(mountain_points)
        seen = set()
        while len(candidates) > 0:
            c = candidates[0]
            candidates.pop(0)
            if c in seen:
                continue
            seen.add(c)
            c.set_temp()
            if c.loc.terrain.height == location.HEIGHT_NONE:
                c.loc.terrain.height = location.HEIGHT_FLAT
            candidates.extend(c.neighbors)
                
        # push rivers
        for point in mountain_points:
            point.push_rivers()

        # for point in self.points:
        #     point.finish()v
            
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

class WorldOpts(object):
    def __init__(self, args, points=None):
        self.point_file = args.point_map_file
        self.num_points = args.num_points
        self.use_points = points
        
class World( object ):
    def __init__( self, opts ):
        if opts.use_points:
            self.points=opts.use_points
        elif opts.point_file:
            self.load_points(opts.point_file)
            self.assign_locations()            
        else:
            self.generate_points( opts.num_points )
            self.assign_locations()            

        self.player_pos = [ random.random(), random.random() ]
        self.target_pos = None
        self.active_loc = None

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
        num_seas = 4
        
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
            #don't iterate twice, but keep this line if get rid of max river depth
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

    def get_fight(self):
        return self.fight
    
    def get_location_actions( self, player ):
        return self.active_loc.loc.get_actions(player)
    
    def increment_travel( self, player ):
        tx, ty = self.target_pos
        px, py = self.player_pos
        s = player.speed
        a = ty - py
        o = tx - px
        h = math.hypot( a, o )
        if h < s:
            self.player_pos = self.target_pos
            self.active_loc = self.points[ self.target_pos ]
            self.target_pos = None
            return self.active_loc
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



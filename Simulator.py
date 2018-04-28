import json, FuelCores, Blocks
import datetime

BlockMap = {
             'U': FuelCores.FissionCore,
             'T': FuelCores.ThoriumCore,
             'B': Blocks.Boiler        ,
             'A': Blocks.Absorber      ,
             'R': Blocks.Reflector     ,
             'S': Blocks.HSLABlock     ,
             'O': Blocks.ObsidianBlock ,
             'W': Blocks.WaterBlock    ,
             'C': Blocks.ConcreteBlock ,
             'I': Blocks.BedIngotBlock ,
             'L': Blocks.LeadBlock     ,
             'G': Blocks.BlastGlassBlock
           }

MsgStyles = [ 'VERBOSE',
              'NORMAL',
              'MINIMAL' ]

def GetNow():
	'''
	Returns the current timestamp in the following format:
	09-March-2018 14:12:11:070
	'''
    fmt = '%d-%b-%Y %H:%M:%S:%f'
    return datetime.datetime.now().strftime( fmt )

def SecsToTicks( secs ):
    '''
    Gets the number of ticks in a given amount of seconds.
    '''
    return int( secs * 20 )

class JSONSerializable():
    '''
    JSONSerializable class.  Allows any child class to have
    its state rendered as a JSON string, as well as allowing
    its state to be reloaded from a provided JSON string.
    '''
    def to_dict( self ):
        '''
        Renders a child object as a dictionary object.
        '''
        return self._traverse_dict( self.__dict__ )

    def _traverse_dict( self, instance_dict ):
        output = {}
        for ( key, value ) in instance_dict.items():
            output[key] = self._traverse( key, value )
        return output

    def _traverse( self, key, value ):
        if isinstance( value, JSONSerializable ):
            return value.to_dict()
        elif isinstance( value, dict ):
            return self._traverse_dict( value )
        elif isinstance( value, list ):
            return [self._traverse( key, i ) for i in value]
        elif hasattr( value, '__dict__' ):
            return self._traverse_dict( value.__dict__ )
        else:
            return value
    
    @classmethod
    def from_json( cls, data ):
        '''
        Restores a child object's state from a JSON string.
        '''
        if ( isinstance( data, str ) == True ):
            kwargs = json.loads( data )
            return cls( **kwargs )
        elif ( isinstance( data, dict ) == True ):
            kwargs = data
            return cls( **kwargs )
        else:
            return cls( **data )

    def to_json( self ):
        '''
        Renders a child object and associated state information
        as a JSON string.
        '''
        return json.dumps( self.to_dict() )

class Reactor( JSONSerializable ):
    '''
    Represents the simple data form of the reactor that can
    be both read from and saved to a JSON string.
    Default has one layer, no blocks, neutron speeds disabled,
    and runs the simlation for 5 minutes (6000 ticks).
    '''
    def __init__( self,
                  layers        = 1,
                  layout        = '',
                  neutronspeeds = False,
                  sim_secs      = 300,
                  message_style = 'VERBOSE' ):
        self.layers        = int( layers )
        self.layout        = str( layout ).upper()
        self.neutronspeeds = bool( neutronspeeds )
        self.sim_ticks     = SecsToTicks( float( sim_secs ) )
        self.message_style = message_style if message_style in MsgStyles \
                             else 'VERBOSE'

class SimEntry( JSONSerializable ):
    '''
    Represents an entry in the simulation logs that is returned
    to the user once the simulation completes.
    '''
    def __init__ ( self,
                   timestamp = 'N/A',
                   tick      = 0,
                   msg       = 'Nope.' ):
        if ( timestamp == 'N/A' or timestamp == None ):
            self.timestamp = GetNow()
        else:
            self.timestamp = timestamp
        self.tick      = tick
        self.msg       = msg
        
    def __str__( self ):
        return '%s; tick %d; %s' % ( self.timestamp, self.tick, self.msg )

class ReactorSim( JSONSerializable ):
    '''
    Represents the proper, simulation-ready form of the
    reactor layout, read in from a Reactor object.
    By default, creates an empty, one-layer reactor that
    runs for 5 minutes (6000 ticks), and does NOT have
    the neutron speed option enabled.
    '''
    def __init__( self, reactor ):
        if ( isinstance( reactor, Reactor ) ):
            self.layers        = reactor.layers
            self.reactor       = []
            self.height        = 0
            self.neutronspeeds = reactor.neutronspeeds
            
            for line in reactor.layout.split( '\n' ):
                self.reactor.append( [] )
                for c in line:
                    if ( c.upper() in BlockMap.keys() ):
                        self.reactor[self.height].append( \
                                    BlockMap[c.upper()]() )
                    else:
                        self.reactor[self.height].append( None )
                self.height += 1

            self.width     = len( self.reactor[0] )
            self.sim_ticks = reactor.sim_ticks
            self.msg_style = reactor.message_style
        else:
            self.layers        = 1
            self.reactor       = [None]
            self.height        = 0
            self.width         = 0
            self.neutronspeeds = False
            self.sim_ticks     = SecsToTicks( 300 )
            self.msg_style     = 'VERBOSE'

    def RunSimulation( self ):
        '''
        Runs the simulation of the reactor, returning all collected
        data from the simulation.
        '''
        sim_data = [SimEntry( tick = -1,
                              msg  = 'Entering main simulation loop.' )]
        for i in range( self.sim_ticks ):
            if ( self.msg_style == 'VERBOSE' ):
                sim_data.append( SimEntry( tick = i,
                                 msg = 'At tick ' + str( i ) + '.' ) )
            
            # NOTES:
            # For each block:
            # - If block is U235/Pu239 core, send out neutrons and
            #    do temperature whatnot.
            # - If block is thorium core, check for temperature and
            #    such, if it does a neutron, good.
            # HOW THE FUCK DO I DO NEUTRONS?
        
        return sim_data
    
    def DoNeutronTravel( self, origin, neutron ):
        '''
        Simulates a single neutron entity travelling through the
        reactor, and interacting with blocks as it goes.
        '''
        if not isinstance( neutron, FuelCores.Neutron ):
            raise 'The simulator tried to make a non-neutron travel!'
        elif len( origin ) != 2:
            raise 'The simulator failed to pass in two coordinates!'
        elif ( origin[0] <  0          or
               origin[1] <  0          or
               origin[0] >= self.width or
               origin[1] >= self.height ):
            raise 'Neutron was out of bounds!  X=%d, Y=%d' % \
                   origin
        else:
            if ( neutron.Direction == 'N' ):
                if ( origin[1] == 0 ):
                    return 'Neutron exited the reactor structure.'
                else:
                    pass
            elif ( neutron.Direction == 'S' ):
                if ( origin[1] == self.height - 1 ):
                    return 'Neutron exited the reactor structure.'
                else:
                    pass
            elif ( neutron.Direction == 'E' ):
                if ( origin[0] == self.width - 1 ):
                    return 'Neutron exited the reactor structure.'
                else:
                    pass
            elif ( neutron.Direction == 'W' ):
                if ( origin[0] == 0 ):
                    return 'Neutron exited the reactor structure.'
                else:
                    pass
            else:
                raise 'Neutron has an invalid direction: %s' % \
                       neutron.Direction
        
    
    def IsShielding( self, x, y ):
        '''
        Returns whether or not the block at a given x and y
        coordinates are a shielding block.
        '''
        if ( x > self.width or y > self.height ):
            return False
        else:
            return issubclass( type( self.reactor[x, y] ),
                               Blocks.Shielding )
            
    def IsFuelCore( self, x, y ):
        '''
        Returns whether or not the block at a given x and y
        coordinates are a fuel core block.
        '''
        if ( x > self.width or y > self.height ):
            return False
        else:
            return issubclass( type( self.reator[x, y] ),
                               FuelCores.FuelCoreBase )
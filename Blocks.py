BoilerFluids = ['WATER', 'AMMONIA']

# These values might not be accurate, check in-game!
ShieldTypes = { 'STEEL':      { 'reflect': 95,
                                'absorb':  90   },
                'CONCRETE':   { 'reflect': 70,
                                'absorb':  60   },
                'WATER':      { 'reflect': 10,
                                'absorb':  30   },
                'BEDROCK':    { 'reflect': 100,
                                'absorb':  97.5 },
                'LEAD':       { 'reflect': 50,
                                'absorb':  75   },
                'OBSIDIAN':   { 'reflect': 80,
                                'absorb':  50   },
                'BLASTGLASS': { 'reflect': 20,
                                'absorb':  80   } }

class Boiler():
    '''
    Represents a boiler (either water or ammonia) within
    the reactor's structure.
    '''
    def __init__( self ):
        self.MaxTemp  = 600
        self.BoilTemp = 100
        self.Temp     = 25
        self.Steam    = 0
        self.Fluid    = 'WATER'

    def CanBoil( self ):
        '''
        Determines if the boiler is capable of boiling its
        internal fluid.
        '''
        return self.Temp >= self.BoilTemp

    def Detonates( self ):
        '''
        Does this fluid detonate, or suffer a hydrogen explosion
        upon meltdown?
        '''
        return self.Fluid == 'AMMONIA'

    @property
    def Fluid( self ):
        return self._Fluid

    @Fluid.setter
    def Fluid( self, f ):
        if f in BoilerFluids:
            self._Fluid = f
        else:
            self._Fluid = 'WATER'

class Reflector():
    '''
    Represents a neutron reflector within the reactor's
    structure.
    '''
    def __init__( self ):
        # TODO: These values are just placeholders!
        self.ReflectChance = 90
        self.AbsorbChance  = 10

class Absorber():
    '''
    Represents a neutron absorber within the reactor's
    structure.  Only really used for fusion, but added
    for completeness.
    '''
    def __init__( self ):
        # TODO: These values are just placeholders!
        self.ReflectChance = 10
        self.AbsorbChance  = 90
        self.Temp          = 25

class Shielding():
    '''
    Represents a form of neutron/radiation shielding
    within the reactor's structure.  Examples include
    HSLA steel blocks, concrete, and bedrock ingot
    blocks.
    '''
    def __init__( self ):
        self.Material = 'STEEL'

    @property
    def Material( self ):
        return self._Material

    @Material.setter
    def Material( self, m ):
        if m in ShieldTypes.keys():
            self._Material = m
        else:
            self._Material = 'STEEL'

class HSLABlock( Shielding ):
    def __init__( self ):
        self.Material = 'STEEL'
    
    @property
    def AbsorbChance( self ):
        return ShieldTypes[self.Material]['absorb']
    
    @property
    def ReflectChance( self ):
        return ShieldTypes[self.Material]['reflect']

class ConcreteBlock( Shielding ):
    def __init__( self ):
        self.Material = 'CONCRETE'
    
    @property
    def AbsorbChance( self ):
        return ShieldTypes[self.Material]['absorb']
    
    @property
    def ReflectChance( self ):
        return ShieldTypes[self.Material]['reflect']
    
class WaterBlock( Shielding ):
    def __init__( self ):
        self.Material = 'WATER'
        
    @property
    def AbsorbChance( self ):
        return ShieldTypes[self.Material]['absorb']
    
    @property
    def ReflectChance( self ):
        return ShieldTypes[self.Material]['reflect']
    
class BedIngotBlock( Shielding ):
    def __init__( self ):
        self.Material = 'BEDROCK'
        
    @property
    def AbsorbChance( self ):
        return ShieldTypes[self.Material]['absorb']
    
    @property
    def ReflectChance( self ):
        return ShieldTypes[self.Material]['reflect']
    
class LeadBlock( Shielding ):
    def __init__( self ):
        self.Material = 'LEAD'
        
    @property
    def AbsorbChance( self ):
        return ShieldTypes[self.Material]['absorb']
    
    @property
    def ReflectChance( self ):
        return ShieldTypes[self.Material]['reflect']
    
class ObsidianBlock( Shielding ):
    def __init__( self ):
        self.Material = 'OBSIDIAN'
        
    @property
    def AbsorbChance( self ):
        return ShieldTypes[self.Material]['absorb']
    
    @property
    def ReflectChance( self ):
        return ShieldTypes[self.Material]['reflect']

class BlastGlassBlock( Shielding ):
    def __init__( self ):
        self.Material = 'BLASTGLASS'
        
    @property
    def AbsorbChance( self ):
        return ShieldTypes[self.Material]['absorb']
    
    @property
    def ReflectChance( self ):
        return ShieldTypes[self.Material]['reflect']
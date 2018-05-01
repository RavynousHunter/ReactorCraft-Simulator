import Helpers
import numpy as np

NeutronTypes = ['FISSION',
                'FUSION',
                'BREEDER',
                'THORIUM',
                'NULL',
                'DECAY',
                'WASTE']

NeutronSpeeds = ['THERMAL',
                 'FAST']

FissionFuels = { 'URANIUM':   { 'fissionChance': 25,
                                'consumeChance':  3,
                                'wasteChance':    5,
                                'tempStep':      20 },
                 'PLUTONIUM': { 'fissionChance': 30,
                                'consumeChance':  4,
                                'wasteChance':   10,
                                'tempStep':      30 } }

Directions = [ 'N', 'S',
               'E', 'W' ]
    

class Neutron:
    '''
    Represents a neutron within the reactor, generated by fuel
    cores.  Interacts with blocks such as other fuel cores and
    boilers.  "Speed" property only ever set if the config is
    enabled; it is disabled by default.
    '''
    def __init__( self,
                  Speed     = 'THERMAL',
                  Type      = 'FISSION',
                  Direction = 'N',
                  Location  = ( 0, 0 ) ):
        self.Speed     = Speed.upper()
        self.Type      = Type.upper()
        self.Direction = Direction.upper()
        self.Location  = Location

    @property
    def Speed( self ):
        return self._Speed

    @Speed.setter
    def Speed( self, s ):
        self._Speed = s if s in NeutronSpeeds else 'THERMAL'

    @property
    def Type( self ):
        return self._Type

    @Type.setter
    def Type( self, t ):
        self._Type = t if t in NeutronTypes else 'FISSION'
        
    @property
    def Direction( self ):
        return self._Direction
    
    @Direction.setter
    def Direction( self, d ):
        self._Direction = d.upper() if d.upper() in Directions else 'N'
        
    @property
    def Location( self ):
      return self._Location
    
    @Location.setter
    def Location( self, loc ):
      if ( loc[0] < 0 ):
        self._Location[0] = 0
      elif ( loc[1] < 0 ):
        self._Location[1] = 0
      else:
        self._Location = loc

    def GetBoilerAbsorptionChance( self ):
        '''
        Gets the chance a boiler will absorb this kind of neutron.
        80% chance if it is a BREEDER or THORIUM type, else 0%.
        (Assumption: Absorption means that it doesn't interact
        with the boiler and generate useful heat.)
        '''
        return 80 if self.Type in ['BREEDER', 'THORIUM'] else 0

    def GetSodiumBoilerAbsorptionChance( self ):
        '''
        Gets the chance a molten sodium boiler will absorb this
        kind of neutron.  0% chance if it is a BREEDER or DECAY
        type, else 90%.
        (Assumption: Absorption means that it doesn't interact
        with the boiler and generate useful heat.)
        '''
        return 0 if self.Type in ['BREEDER', 'DECAY'] else 90

    def CanTriggerFuelConversion( self ):
        '''
        Can this kind of neutron convert breeder fuel into
        plutonium?
        '''
        return self.Type == 'BREEDER'

    def DealsDamage( self ):
        '''
        Are living things harmed by this kind of neutron?
        '''
        return self.Type != 'NULL'

    def StoppedByWater( self ):
        '''
        Is this kind of neutron stopped by water?
        '''
        return self.Type != 'FUSION'

    def CanIrradiateLiquids( self ):
        '''
        Can this kind of neutron irradiate liquids that it hits?
        '''
        return self.Type in ['FISSION', 'FUSION', 'BREEDER', 'THORIUM']

    def IsFissionType( self ):
        '''
        Is this kind of neutron the result of nuclear fission?
        '''
        return self.Type in ['DECAY', 'FISSION', 'BREEDER', 'THORIUM']

    def CanTriggerFission( self ):
        '''
        Can this kind of neutron trigger fission?  If
        IsFissionType() returns True, it does.  If it
        is a WASTE type, 40% chance.  Else, it does not.
        '''
        if ( self.IsFissionType() ):
            return True
        else:
            if ( self.Type == 'WASTE' and Helpers.DoWithChance( 40 ) ):
                return True
            else:
                return False

    def GetInteractionMultiplier( self ):
        '''
        Get the chance of interaction between this speed of neutron
        and other objects.  FAST neutrons have 0.6x multiplier,
        THERMAL neutrons have 1.0x multiplier.  Only used if neutron
        speed categories are enabled.
        '''
        return 0.6 if self.Speed == 'FAST' else 1

    def GetIrradiatedAbsorptionChance( self ):
        '''
        Unknown.  Maybe the chance this speed of neutron gets
        absorbed by irradiated blocks?  FAST neutrons have 40%
        chance of absorption, THERMAL neutrons have 100% chance.
        Only used if neutron speed categories are enabled.
        '''
        return 40 if self.Speed == 'FAST' else 100

    def GetWasteConversionMultiplier( self ):
        '''
        How much more likely a given speed of neutron is to
        cause a core to generate waste.  THERMAL neutrons have
        a 1.0x multiplier, FAST neutrons have a 2.2x multiplier.
        Only used if neutron speed categories are enabled.
        '''
        if ( self.Speed == 'THERMAL' ):
            return 1
        if ( self.Speed == 'FAST' ):
            return 2.2
        return 0

class FuelCoreBase:
    '''
    The base class used by other fuel cores to define their common
    data members and behaviours.
    '''
    def __init__( self,
                  UsesFluidFuel  = False,
                  FluidUseRate   = 0,
                  WasteOutRate   = 0,
                  HotFuelOutRate = 0,
                  MinTemp        = 0,
                  MaxTemp        = 1400,
                  MeltDownTemp   = 2000,
                  MeltsDown      = True ):
        self.UsesFluidFuel  = UsesFluidFuel
        self.FluidUseRate   = FluidUseRate
        self.WasteOutRate   = WasteOutRate
        self.HotFuelOutRate = HotFuelOutRate
        self.MinTemp        = MinTemp
        self.MaxTemp        = MaxTemp
        self.MeltsDown      = MeltsDown

    def OnNeutron( self, neutron ):
        '''
        Defines how the fuel core interacts with a neutron.
        '''
        pass

    def GetNeutronInteractionChance( self ):
        '''
        Defines the percentage chance of neutron interactions
        with a fuel core block.
        '''
        pass

    def GetNeutronChance( self ):
        '''
        Defines the percentage chance for a fuel core block
        to emit a neutron of its own.
        '''
        pass
    
    def SpawnNeutron( self ):
        '''
        Causes the fuel core to spawn a neutron of the appropriate
        type.  Neutrons only travel HORIZONTALLY across the reactor.
        '''
        pass

class ThoriumCore( FuelCoreBase ):
    '''
    Defines a fuel core for a LFTR (Liquid Fluoride Thorium Reactor).
    '''
    def __init__( self ):
        self.UsesFluidFuel  = True
        self.FluidUseRate   = 100
        self.WasteOutRate   = 50
        self.HotFuelOutRate = 100
        self.MinTemp        = 400
        self.MaxTemp        = 1200
        self.MeltDownTemp   = -1
        self.MeltsDown      = False

        self.Temp = 25

    def GetNeutronInteractionChance( self ):
        '''
        Runs a cos-interpolation between 400 & 1200C at
        the core's current temperature.
        '''
        return Helpers.CosInterpolate( self.MinTemp,
                                       self.MaxTemp,
                                       self.Temp )

    def GetNeutronChance( self ):
        return 25 - 20 * np.sqrt( ( self.Temp    - self.MinTemp ) / \
                                  ( self.MaxTemp - self.MinTemp ) )

    def OnNeutron( self, neutron ):
        if ( isinstance( neutron, type( Neutron ) ) ):
            if ( neutron.CanTriggerFission() and
                 Helpers.DoWithChance( neutron.GetInteractionMultiplier() ) and
                 ( neutron.Type != 'BREEDER' and
                   Helpers.DoWithChance( self.GetNeutronInteractionChance() ) ) ):
                
                if ( Helpers.DoWithChance( self.GetNeutronChance() ) ):
                    # Consume fuel, make hot fuel.
                    self.Temp += 20
                    if ( Helpers.DoWithChance( 5 ) ):
                        self.AddWaste()
                return { 'success':  True,
                         'neutrons': [self.SpawnNeutron() for _
                                      in range( 3 )] }
            else:
                return { 'success':  False,
                         'neutrons': None }
        else:
            raise 'Neutron was not a neutron!'

    def AddWaste( self ):
        '''
        Add waste to the LFTR fuel core; TBA.
        '''
        pass
    
    def SpawnNeutron( self ):
        N = Neutron( Speed     = 'THERMAL',
                     Type      = 'THORIUM',
                     Direction = Helpers.PickFromList( Directions ) )
        
        return N

class FissionCore( FuelCoreBase ):
    '''
    Defines a fuel core for a standard (U-235/Pu-239) nuclear
    fission reactor.
    '''
    def __init__( self ):
        self.UsesFluidFuel  = False
        self.FluidUseRate   = -1
        self.WasteOutRate   = -1
        self.HotFuelOutRate = -1
        self.MinTemp        = 0
        self.MaxTemp        = 1400
        self.MeltsDown      = True
        self.MeltDownTemp   = 1800

        self.Temp     = 25
        self.Hydrogen = 0
        self.Fuel     = 'URANIUM'

    def GetNeutronInteractionChance( self ):
        '''
        Just returns 1; neutrons ALWAYS interact with this block,
        regardless of type.
        '''
        return 1

    def GetNeutronChance( self ):
        '''
        Returns either 25% or 30%, depending on whether or not
        the core is using U-235 or Pu-239, respectively.
        '''
        return FissionFuels[self.Fuel]['fissionChance']

    def OnNeutron( self, neutron ):
        if ( isinstance( neutron, type( Neutron ) ) ):
            if ( neutron.CanTriggerFission() and
                 Helpers.DoWithChance( neutron.GetInteractionMultiplier() ) ):
                if ( Helpers.DoWithChance( self.GetNeutronChance() ) ):
                    # When the time comes, fuel/waste goes here.
                    self.Temp += FissionFuels[self.Fuel]['tempStep']
                    # TODO: Need to check for meltdown/hydrogen conditions!
                    return { 'success':  True,
                             'neutrons': [self.SpawnNeutron() for _
                                          in range( 3 )] }
                else:
                    return { 'success':  False,
                             'neutrons': None }
            else:
                return { 'success':  False,
                         'neutrons': None }
        else:
            raise 'Neutron was not a neutron!'

    def SpawnNeutron( self ):
        N = Neutron( Speed     = 'THERMAL',
                     Type      = 'FISSION',
                     Direction = Helpers.PickFromList( Directions ) )
        return N

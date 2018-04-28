import random as rand
import numpy  as np

def CosInterpolate( lower, upper, value ):
    if ( lower <= value <= upper ):
        size = ( upper - lower ) / 2
        mid  = lower + size

        if ( value == mid ):
            return 1
        else:
            return 0.5 + 0.5 * np.cos(
                np.radians( ( value - mid ) /  size * 180 ) )
    else:
        return 0

def DoWithChance( value ):
    if ( value >= 100 ):
        return True
    if ( value > 1 ):
        value /= 100
    if ( value >= 1 ):
        return True
    if ( value <= 0 ):
        return False
    if ( value < 1.0e-014 ):
        return rand.random() * 1e13 < value * 1e13
    return rand.random() < value

def PickFromList( lst ):
    if ( not isinstance( lst, list ) ):
        return None
    else:
        val = rand.randint( 0, len( lst ) - 1 )
        return lst[val]
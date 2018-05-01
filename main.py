from Simulator import Reactor, ReactorSim
from flask     import request, url_for
from flask_api import FlaskAPI, status, exceptions

import json

app = FlaskAPI( __name__ )

def ValidateJSON( data ):
    '''
    Validate the JSON dictionary passed to the method
    to ensure that it actually *is* a Reactor object.
    '''
    if ( data == None ):
        return False

    parts = ['layers',        'layout',
             'neutronspeeds', 'sim_secs']
    
    for part in parts:
        if ( not part in data.keys() ):
            return False
    
    return True

def ValidateReactor( reactor ):
    '''
    Ensures that a reactor can actually run before
    wasting time trying to simulate it.
    '''
    if ( isinstance( reactor, Reactor ) == False ):
        return { 'success': False,
                 'reason': 'Not a reactor!  THIS IS REALLY BAD!' }
    if ( reactor.layers < 1 ):
        return { 'success': False,
                 'reason': 'Need more than one layer!' }
    if ( 'U' not in reactor.layout and
         'T' not in reactor.layout ):
        return { 'success': False,
                 'reason': 'No fuel cores!' }
    if ( 'B' not in reactor.layout ):
        return { 'success': False,
                 'reason': 'No boilers!' }
    if ( reactor.sim_ticks < 1 ):
        return { 'success': False,
                 'reason': 'You need to simulate for at least 1 tick!' }
    
    return { 'success': True,
             'reason': "I ain't broke." }

@app.route( '/', methods = ['POST'] )
def Simulation():
    data = request.get_json()
    print( 'data: ', data )
    if ( ValidateJSON( data ) == False ):
        return { 'Error': 'Data passed was not valid Reactor data.',
                 'data':   data }
    else:
        R          = Reactor.from_json( data )
        validation = ValidateReactor( R )
        if ( validation['success'] == False ):
            return { 'Error': validation['reason'],
                     'data':  data,
                     'R':     R.to_json() }
        else:
            Sim  = ReactorSim( R )
            data = Sim.RunSimulation()
            return { 'Message': 'Ya did good!',
                     'data':     data,
                     'R':        R.__dict__,
                     'sim_data': data }

if __name__ == '__main__':
    app.run( debug = True )

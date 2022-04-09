#!/usr/bin/env python

"""
 @Programmer(s)
    Kenneth A. Jones II
    kejo1166@colorado.edu

 @Company
    University of Colorado Boulder

@Description
    Script with commonly use methods

@Reference
    None

"""

import time

def get_elasped_time(start_time, current_time):
    ''' Get the elapsed amount of time

    :param start_time: Start time
    :param current_time: Current time
    '''
    return current_time - start_time

def degree_c_to_degree_f(temp_c):
    ''' Converts temperature from C to F

    :param temp_c: Temperature in C
    '''
    return temp_c * 1.8 + 32.0

def mbar_to_inhg(mbars):
    ''' Converts millibars to inHg

    '''
    return mbars * 0.029530
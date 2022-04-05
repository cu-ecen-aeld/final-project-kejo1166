#!/usr/bin/env python

"""
 @Programmer(s)
    Kenneth A. Jones II
    kejo1166@colorado.edu

 @Company
    University of Colorado Boulder

@Description
    Simple test script for all sense hat sensors

@Reference
    None

"""

import os
import sys

# Ensure lib added to path, before any other imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import argparse
import signal
import sys
import time

import sensehatlive.log.logger as logger
from sense_hat import SenseHat


def sig_handler(signum=None, frame=None):
    ''' Signal handler

    :param signum: Signal responsible for call back
    :return:
    '''
    if signum is not None:
        logger.info("Signal %i caught, exiting...", signum)

    # Clear exit
    sys.exit()


def main(args):
    ''' Main function

    :param args: Command line arguments
    :return:
    '''

    # Register signals
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    # Initialize the logger
    logger.initLogger(console=not args.quiet, log_dir=False, verbose=args.verbose)

    rc = 0
    try:
        logger.info('Sense Hat Live!: Test')
        sh = SenseHat()
        while True:
            logger.info('Temperature = {:.1f} °C'.format(sh.get_temperature()))
            logger.info('Humidity = {} %rH'.format(int(sh.get_humidity())))
            logger.info('Pressure = {:.1f} mBar'.format(sh.get_pressure()))
            logger.info('Orientation = p: {pitch:.1f}, r: {roll:.1f}, y: {yaw:.1f}'.format(**sh.get_orientation()))
            logger.info('Compass = N {:.1f}'.format(sh.get_compass()))
            logger.info('Acceleration = p: {pitch:.1f}, r: {roll:.1f}, y: {yaw:.1f}'.format(**sh.get_accelerometer()))
            time.sleep(1)

    except Exception as e:
        logger.error('Exception caught: ' + str(e))

    sys.exit(rc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sense HAT Live! - Producer')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase console logging verbosity')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Turn off console logging')
    args = parser.parse_args()
    main(args)

#!/usr/bin/env python

"""
 @Programmer(s)
    Kenneth A. Jones II
    kejo1166@colorado.edu

 @Company
    University of Colorado Boulder

@Description
    Main application entry script

@Reference
    None

"""

import os
import sys

# Ensure lib added to path, before any other imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib/'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sensehatlive/'))

import argparse
import signal
import sys
import time

import sensehatlive.log.logger as logger
from sensehatlive.sensemanager.manager import SenseHatManager

sh = None

def sig_handler(signum=None, frame=None):
    ''' Signal handler

    :param signum: Signal responsible for call back
    :return:
    '''
    if signum is not None:
        logger.info("Signal %i caught, exiting...", signum)

    if sh is not None:
        sh.stop()
        sh.join()

    # Clear exit
    sys.exit()


def main(args):
    ''' Main function

    :param args: Command line arguments
    :return:
    '''
    global sh

    # Register signals
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    # Initialize the logger
    logger.initLogger(console=not args.quiet, log_dir=False, verbose=args.verbose)

    rc = 0
    try:
        logger.info('Sense Hat Live!: Producer')
        sh = SenseHatManager()
        sh.start()

        while True:
            #TODO: Add code for main thread task
            time.sleep(1)

    except Exception as e:
        logger.error('Exception caught: ' + str(e))

    sh.stop()
    sh.join()
    sys.exit(rc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sense HAT Live! - Producer')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase console logging verbosity')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Turn off console logging')
    args = parser.parse_args()
    main(args)

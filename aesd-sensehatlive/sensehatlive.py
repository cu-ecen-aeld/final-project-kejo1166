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

import sensehatlive
import argparse
import signal
import sys
import time

import sensehatlive.log.logger as logger
from sensehatlive.sensemanager.manager import SenseHatManager

sh = None

# Register signals
signal.signal(signal.SIGINT, sensehatlive.sig_handler)
signal.signal(signal.SIGTERM, sensehatlive.sig_handler)

def main(args):
    ''' Main function

    :param args: Command line arguments
    :return:
    '''
    global sh

    sensehatlive.VERBOSE = args.verbose
    sensehatlive.QUIET = args.quiet

    # Initialize the logger
    logger.initLogger(console=not sensehatlive.QUIET, log_dir=os.path.dirname(__file__), verbose=sensehatlive.VERBOSE)

    if args.daemon:
        logger.warning('Overriding quiet option when daemonizing')
        sensehatlive.DAEMON = True
        sensehatlive.QUIET = True

    if args.pidfile:
        sensehatlive.PIDFILE = str(args.pidfile)

        # If the pidfile already exists, sense hat live may still be running, so exit
        if os.path.exists(sensehatlive.PIDFILE):
            msg = "PID file '{}' already exists. Exiting.".format(sensehatlive.PIDFILE)
            logger.warning(msg)
            raise SystemExit(msg)

        # The pidfile is only useful in daemon mode, make sure we can write the file properly
        if sensehatlive.DAEMON:
            sensehatlive.CREATEPID = True

            try:
                with open(sensehatlive.PIDFILE, 'w') as fp:
                    fp.write("pid\n")
            except IOError as e:
                msg ="Unable to write PID file: {}".format(e)
                logger.warning(msg)
                raise SystemExit(msg)

        else:
            logger.warn("Not running in daemon mode. PID file creation disabled.")

    if sensehatlive.DAEMON:
        sensehatlive.daemonize()

    logger.info('Sense Hat Live!: Producer')
    sh = SenseHatManager()
    sensehatlive.insert_thread(sh)

    # Start all threads
    sensehatlive.start_threads()

    while True:
        if not sensehatlive.SIGNAL:
            try:
                time.sleep(1)

            except KeyboardInterrupt:
                sensehatlive.SIGNAL = 'shutdown'
                sensehatlive.stop_threads()

        else:
            logger.info('Received signal: {}', sensehatlive.SIGNAL)
            sensehatlive.stop_threads()

            if sensehatlive.SIGNAL == 'shutdown':
                sensehatlive.shutdown()
            sensehatlive.SIGNAL = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sense HAT Live! - Producer')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase console logging verbosity')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Turn off console logging')
    parser.add_argument('-d', '--daemon', action='store_true',
                        help='Run as a daemon')
    parser.add_argument('--pidfile',
                        help='Create a pid file (only relevant when running as a daemon)')
    args = parser.parse_args()
    main(args)

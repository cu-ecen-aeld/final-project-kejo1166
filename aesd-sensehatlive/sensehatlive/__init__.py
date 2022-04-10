#!/usr/bin/env python

"""
 @Programmer(s)
    Kenneth A. Jones II
    kejo1166@colorado.edu

 @Company
    University of Colorado Boulder

@Description
    Sense hat globals

@Reference
    None

"""

import os
import sys
import threading
from sensehatlive.log import logger

# Application globals
APP_NAME = 'Sense Hat Live!'
SIGNAL = None
QUIET = False
VERBOSE = False
DAEMON = False
CREATEPID = False
PIDFILE = None
THREADS = []

def sig_handler(signum=None, frame=None):
    ''' Signal handler

    :param signum: Signal responsible for call back
    :return:
    '''
    if signum is not None:
        logger.info("Signal %i caught, exiting...", signum)
        stop_threads()
        shutdown()

def insert_thread(thread):
    ''' Add threads to list

    :params thread: Thread to add
    '''
    global THREADS

    THREADS.append(thread)

def start_threads():
    ''' Starts threads

    '''

    for t in THREADS:
        t.start()

def stop_threads():
    ''' Stops threads

    '''

    for t in THREADS:
        t.stop()
        t.join()

def shutdown(restart=False, update=False, exit=True):
    ''' Shutdown system

    :param restart: Restart system
    :param update: Update code
    :param exit: Exit application
    '''
    if not restart and not update:
        logger.info(APP_NAME + ' is shutting down...')

    if update:
        logger.info('Update not implemented')

    if CREATEPID:
        logger.info('Removing pidfile {}'.format(PIDFILE))
        os.remove(PIDFILE)

    if restart:
        logger.info('Restart not implemented')

    if exit:
        sys.exit()

def daemonize():
    ''' Run application as daemon

    '''
    if threading.activeCount() != 1:
        logger.warn('There are {} active threads. Daemonizing may cause strange behavior.'.format(
            threading.enumerate()))

    sys.stdout.flush()
    sys.stderr.flush()

    # Do first fork
    try:
        pid = os.fork()  # @UndefinedVariable - only available in UNIX
        if pid != 0:
            sys.exit(0)
    except OSError as e:
        raise RuntimeError("1st fork failed: {} [{}]".format(e.strerror, e.errno))

    os.setsid()

    # Make sure I can read my own files and shut out others
    prev = os.umask(0)  # @UndefinedVariable - only available in UNIX
    os.umask(prev and int('077', 8))

    # Make the child a session-leader by detaching from the terminal
    try:
        pid = os.fork()  # @UndefinedVariable - only available in UNIX
        if pid != 0:
            sys.exit(0)
    except OSError as e:
        raise RuntimeError("2nd fork failed: {} [{}]".format(e.strerror, e.errno))

    dev_null = open('/dev/null', 'r')
    os.dup2(dev_null.fileno(), sys.stdin.fileno())

    si = open('/dev/null', "r")
    so = open('/dev/null', "a+")
    se = open('/dev/null', "a+")

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    pid = os.getpid()
    logger.info('Daemonized to PID: %d', pid)

    if CREATEPID:
        logger.info("Writing PID {} to {}".format(pid, PIDFILE))
        with open(PIDFILE, 'w') as fp:
            fp.write("{}\n".format(pid))
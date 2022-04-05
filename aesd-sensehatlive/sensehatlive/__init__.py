#!/usr/bin/env python

"""
 @Programmer(s)
    Kenneth A. Jones II
    kejo1166@colorado.edu

 @Company
    University of Colorado Boulder

@Description
    Class for raspberry pi sense hat

@Reference
    None

"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import threading
import time
import sensehatlive.log.logger as logger

# Defaults
DEFAULT_SAMPLE_INTERVAL_SEC = 10

class SenseManager(threading.Thread):
    ''' Class to manage sense hat sensors
    '''

    def __init__(self, sample_period_sec=DEFAULT_SAMPLE_INTERVAL_SEC):
        ''' Initialize class

        :param sample_period_sec: Sample period for sense hat sensors
        '''
        # Base class initialization
        super(SenseManager, self).__init__()
        self._shutdown = False
        self._interval = sample_period_sec if sample_period_sec >= DEFAULT_SAMPLE_INTERVAL_SEC else DEFAULT_SAMPLE_INTERVAL_SEC

    def run(self):
        ''' Overrides threading run() method

        :return:
        '''
        logger.info('Sense har manager thread started')
        while not self._shutdown:

            time.sleep(self._interval)

        logger.info('Sense har manager thread stopped')

    def stop(self):
        ''' Shuts down running thread

        :return:
        '''
        logger.info('Stopping sense hat manager ...')
        self._shutdown = True
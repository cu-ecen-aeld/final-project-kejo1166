#!/usr/bin/env python

"""
 @Programmer(s)
    Kenneth A. Jones II
    kejo1166@colorado.edu

 @Company
    University of Colorado Boulder

@Description
    Class for managing a raspberry pi sense hat

@Reference
    Sense HAT API Reference (https://pythonhosted.org/sense-hat/api/)

"""
import os
import json
import time
import threading
import utils
import log.logger as logger
from sense_hat import SenseHat

#LED colors
LED_OFF = (0,0,0)
LED_RED = (255,0,0)
LED_GREEN = (0,255, 0)
LED_BLUE = (0,0,255)

# Defaults
DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), 'default.json')
SENSE_HAT_CONFIG = os.path.join(os.path.dirname(__file__), 'config.json')
TICKS = .500
TICKS_1SEC = 1 / TICKS
TICKS_30SEC = 30 / TICKS




class SenseHatManager(threading.Thread):
    ''' Class to manage sense hat sensors and publication of data

    '''

    def __init__(self, config_path=SENSE_HAT_CONFIG):
        ''' Class initialization

        :param config_path: Path to sense hat configuration
        '''
        super(SenseHatManager, self).__init__()  # Base class initialization

        # Set class defaults
        self._shutdown = False
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.compass = 0
        self.orientation = {'pitch': 0, 'roll': 0, 'yaw': 0}
        self.accelerometer = {'pitch': 0, 'roll': 0, 'yaw': 0}

        # Get instance of sense hat
        self._sh = SenseHat()

        # Load the sense hat config
        self._config = self._load_config(config_path)

        self._sh.clear()

    def run(self):
        ''' Override threading run method

        '''

        logger.info("Sense hat manager thread started")
        n_1sec_ticks = TICKS_1SEC
        while not self._shutdown:
            self._heartbeat() #heartbeat

            if n_1sec_ticks >= TICKS_1SEC:
                n_1sec_ticks = 0

                # update all configured sensors
                for sensor in self._config:
                    self._update_sensor(sensor)

            time.sleep(TICKS)
            n_1sec_ticks += 1

        logger.info("Sense hat manager thread stopped")

    def stop(self):
        ''' Stops the sense hat manager thread

        '''
        logger.debug("Stopping ...")
        self._shutdown = True

    def _heartbeat(self):
        ''' Heartbeat for device

        '''
        color = self._sh.get_pixel(0,0)
        color = LED_RED if color[0] == 0 else LED_OFF
        self._sh.set_pixel(0, 0, color)

    def _load_config(self, path):
        ''' Loads the sense hat configuration from file

        :param path: Path to load file
        '''
        if not os.path.exists(path):
            if not self._default_config(path):
                raise Exception("The sense hat config could not be loaded")

        # Path to config was found or default config was created
        try:
            with open(path) as f:
                data = json.load(f)
                logger.debug('Sense had config successfully loaded')
                return data
        except Exception as e:
            raise Exception(str(e))

    def _default_config(self, path):
        ''' Create a default sense hat configuration and saves to default

        :param path: Path to save file
        '''
        try:
            with open(DEFAULT_CONFIG) as f:
                config = json.load(f)

            with open(path, 'w') as f:
                f.writelines(json.dumps(config))
        except Exception as e:
            logger.error("Could not create default config file, Reason=" + str(e))
            return False

        return True

    def _get_sensor_cfg(self, sensor_name):
        ''' Get the sensor config data

        :param sensor_name: Sensor name
        '''
        cfg = self._config.get(sensor_name)
        if cfg is None:
            raise Exception("Sensor {} configuration is missing".format(sensor_name))

        return cfg

    def _format_val(self, cfg, val):
        ''' Converts value to new type

        :param cfg: Sensor configuration
        :param val: Current value

        :return Formated value
        '''
        if cfg['type'] == 'float':
            return round(float(val), cfg['precision'])
        elif cfg['type'] == 'int':
            return int(val)
        elif cfg['type'] == 'dict':
            pass
        else:
            return val

    def _update_sensor(self, cfg):
        ''' Handles updating sensor values

        :param cfg: sensor configuration
        '''

        if cfg['name'] == 'temperature':
            val = utils.degree_c_to_degree_f(self._sh.get_temperature()) \
                if cfg['units'] == 'F' else self._sh.get_temperature()
            self.temperature = self._process_sensor_val(cfg, val, self.temperature)

        elif cfg['name'] == 'humidity':
            val = self._sh.get_humidity()
            self.humidity = self._process_sensor_val(cfg, val, self.humidity)

        elif cfg['name'] == 'pressure':
            if cfg['units'] == 'inHg':
                val = utils.mbar_to_inhg(self._sh.get_pressure())
            else:
                val = self._sh.get_pressure()
            self.pressure = self._process_sensor_val(cfg, val, self.pressure)

        elif cfg['name'] == 'orientation':
            val = self._sh.get_orientation()
            self.orientation = self._process_imu_vals(cfg, val, self.orientation)

        elif cfg['name'] == 'compass':
            val = self._sh.get_compass()
            self.compass = self._process_sensor_val(cfg, val, self.compass)

        elif cfg['name'] == 'accelerometer':
            self._sh.set_imu_config(False, False, True)  # gyroscope only
            val = self._sh.get_accelerometer()
            self.accelerometer = self._process_imu_vals(cfg, val, self.accelerometer)

        else:
            return

    def _process_sensor_val(self, cfg, new_val, old_val):
        ''' Processes the sensors value

        :param cfg: Sensor config
        :param new_val: New sensor value
        :param old_val: old sensor value

        :return: New sensor value
        '''

        # Format value
        new_val = self._format_val(cfg, new_val)

        # Determine amount of change in value
        delta = abs(new_val - old_val)
        if delta >= cfg['cos_threshold']:
            logger.info("New {} value: {} {}".format(cfg['name'], new_val, cfg['units']))
        return new_val

    def _process_imu_vals(self, cfg, new_val, old_val):
        ''' Processes the imu sensors values

        :param cfg: Sensor config
        :param new_val: New sensor values
        :param old_val: old sensor values

        :return: New sensor values
        '''

        # Format value

        delta = []
        for k, v in new_val.items():
            t = self._format_val(cfg, v)
            new_val[k] = t
            # Determine amount of change in value
            delta.append(abs(new_val[k] - old_val[k]))

        for d in delta:
            if d >= cfg['cos_threshold']:
                logger.info("New {} value: pitch: {}, roll: {}, yaw: {} {}".format(cfg['name'],
                                                                            new_val['pitch'],
                                                                            new_val['roll'],
                                                                            new_val['yaw'],
                                                                            cfg['units']))
        return new_val
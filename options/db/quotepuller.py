"""
.. Copyright (c) 2016 Marshall Farrier
   license http://opensource.org/licenses/MIT

Save data for specific diagonal butterflies.
"""

import logging
import os

import pynance as pn

import config
import constants
import dbwrapper
from trackfinder import TrackFinder

class QuotePuller(object):

    def __init__(self):
        self.logger = logging.getLogger('dgb_save')
        loglevel = logging.INFO if config.ENV == 'prod' else logging.DEBUG
        self.logger.setLevel(loglevel)
        log_dir = _make_log_dir()
        handler = logging.FileHandler(os.path.join(log_dir, 'service.log'))
        formatter = logging.Formatter(constants.LOG_FMT)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def run(self):
        self.logger.debug('running')
        self.logger.info('information')
        tracked = self.gettracked()
        quotes = self.getquotes(tracked)
        self.save(quotes)

    def gettracked(self):
        pass

    def getquotes(self, tracked):
        pass

    def save(self, quotes):
        pass

def _getlogger():
    logger = logging.getLogger('quotepuller')
    loglevel = logging.INFO if config.ENV == 'prod' else logging.DEBUG
    logger.setLevel(loglevel)
    log_dir = _getlogdir()
    handler = logging.FileHandler(os.path.join(log_dir, 'service.log'))
    formatter = logging.Formatter(constants.LOG['format'])
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def _getlogdir():
    log_dir = os.path.normpath(os.path.join(config.LOG_ROOT, constants.LOG['path']))
    try:
        os.makedirs(log_dir)
    except OSError:
        if not os.path.isdir(log_dir):
            raise
    return log_dir

def _run():
    logger = _getlogger()
    trackfinder = TrackFinder(logger)
    print(trackfinder.get())

if __name__ == '__main__':
    _run()
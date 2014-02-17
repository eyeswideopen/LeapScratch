# -*- coding: utf-8 -*-

import ConfigParser

class Config(object):
    """ class for reading information from beast-arena.conf file """
    config = ConfigParser.SafeConfigParser()
    try:
        config.read('../../config')
    except ConfigParser.ParsingError, err:
        print 'Could not parse:', err
    except Exception as e:
    	print e

    def __init__(self):
        """
        instantiation of Config.py is not possible
        """
        errorMessage = 'Instantiation of ' + type(self).__name__ \
            + ' is not possible'
        raise TypeError, errorMessage

    @staticmethod
    def __getScratchFilePath__():
        '''@return the value of startEnergy in config file'''
        return str(Config.config.get('files', 'scratch'))

    @staticmethod
    def __getBaseFilePath__():
        '''@return the value of startEnergy in config file'''
        return str(Config.config.get('files', 'base'))


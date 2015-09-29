"""
/*---------------------------------------------------------------------------
                                Event Logger
 ---------------------------------------------------------------------------*/
"""
from datetime import datetime
from PyQt4 import QtCore
import logging
from PyQt4.QtCore import SIGNAL
from multiprocessing import Queue


class EventLogger():
    """
        Basic EventLogger class.
    """
    
    # Logger Options
    EVENT_CONSOLE_LOGGING = True # for logging to the console
    EVENT_FILE_LOGGING = True  # for event logging in to a file
    EVENT_FILE_LOGGING_PATH = "../eventlogger.log"  # default file path for logging events
    EVENT_LOG_LEVEL = logging.DEBUG
    
    format = "%(asctime)s - %(levelname)8s - %(message)s"
    __loggers = {}
    
    def add_logger(logger):
        if logger.name is None or logger.name == "":
            raise Exception("Logger has no Attribute called 'name'!")

        EventLogger.__loggers[logger.name] = logger
    
    def remove_logger(logger_name):
        if EventLogger.__loggers.has_key(logger_name):
            EventLogger.__loggers.pop(logger_name)
            return True
        
        return False
    
    def debug(msg, logger_name=None):
        level = logging.DEBUG
        EventLogger._send_message(level, msg, logger_name)
        
    def info(msg, logger_name=None):
        level = logging.INFO
        EventLogger._send_message(level, msg, logger_name)
        
    def warn(msg, logger_name=None):
        level = logging.WARN
        EventLogger._send_message(level, msg, logger_name)
        
    def warning(msg, logger_name=None):
        level = logging.WARNING
        EventLogger._send_message(level, msg, logger_name)
        
    def error(msg, logger_name=None):
        level = logging.ERROR
        EventLogger._send_message(level, msg, logger_name)
        
    def critical(msg, logger_name=None):
        level = logging.CRITICAL
        EventLogger._send_message(level, msg, logger_name)
    
    def log(level, msg, logger_name=None):
        EventLogger._send_message(level, msg, logger_name)
    
    def _send_message(level, msg, logger_name):
        if logger_name is not None:
            if EventLogger.__loggers.has_key(logger_name):
                EventLogger.__loggers[logger_name].log(level, msg)
        else:
            for logger in EventLogger.__loggers.values():
                logger.log(level, msg)
    
    
    # static methods
    add_logger = staticmethod(add_logger)
    remove_logger = staticmethod(remove_logger)
    debug = staticmethod(debug)
    info = staticmethod(info)
    warn = staticmethod(warn)
    warning = staticmethod(warning)
    error = staticmethod(error)
    critical = staticmethod(critical)
    log = staticmethod(log)
    _send_message = staticmethod(_send_message)
      
class ConsoleLogger(logging.Logger):
    '''
    This class outputs the logged events to the console
    '''
    
    def __init__(self, name, log_level):
        logging.Logger.__init__(self, name, log_level)
        
        # create console handler and set level
        ch = logging.StreamHandler()
        
        ch.setLevel(log_level)
        
        # create formatter
        formatter = logging.Formatter(EventLogger.format)
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.addHandler(ch)

class FileLogger(logging.Logger):
    '''
    This class writes the logged events to an LOG file (EventLogger.EVENT_FILE_LOGGING_PATH)
    '''
    
    def __init__(self, name, log_level, filename):
        logging.Logger.__init__(self, name, log_level)
        
        ch = logging.FileHandler(filename, mode="a")
        
        ch.setLevel(log_level)
        
        # create formatter
        formatter = logging.Formatter(EventLogger.format)
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.addHandler(ch)
        
        self.info("###### NEW LOGGING SESSION STARTED ######")
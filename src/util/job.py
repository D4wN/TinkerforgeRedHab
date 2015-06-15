""""
/*---------------------------------------------------------------------------
                                Jobs
 ---------------------------------------------------------------------------*/
"""
from src.util.event_logger import EventLogger

import Queue, threading



class AbstractJob(threading.Thread):
    
    def __init__(self, updater=None,  group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self._exit_flag = False
        self._job_name = "[Job:" + self.name + "]"

        self._updater = updater
    
    def stop(self):
        self._exit_flag = True
    
    def _job(self):
        # check for needed objects
        if self._updater is None:
            return False;

        return True



class UpdateItemJob(AbstractJob):
    def __init__(self, updater=None, group=None, name="UpdateItemJob", args=(), kwargs=None, verbose=None):
        target = self._job

        AbstractJob.__init__(self, updater=updater, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        
    def _job(self):
        # check for needed objects
        if not AbstractJob._job(self):
            EventLogger.critical(str(self.name) + " stopped!!")
            return

        EventLogger.debug(str(self._job_name) + " updater="+str(self._updater))
        EventLogger.debug(str(self._job_name) + " TODO: send REST to Items!")

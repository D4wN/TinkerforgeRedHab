""""
/*---------------------------------------------------------------------------
                                Jobs
 ---------------------------------------------------------------------------*/
"""
from src.util.event_logger import EventLogger

import Queue, threading



class AbstractJob(threading.Thread):
    
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self._exit_flag = False
        self._job_name = "[Job:" + self.name + "]"
        
        if self._datalogger is not None:
            self._datalogger.data_queue[self.name] = Queue.Queue()
    
    def stop(self):
        self._exit_flag = True

    
    def _job(self):
        # check for needed objects
        return True

class JobImple(AbstractJob): #TODO better name
    def __init__(self, group=None, name="CSVWriterJob", args=(), kwargs=None, verbose=None):
        target = self._job
        AbstractJob.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        
    def _job(self):
        # check for needed objects
        if AbstractJob._job(self):
            return

        EventLogger.debug(str(self._job_name) + " NYI")

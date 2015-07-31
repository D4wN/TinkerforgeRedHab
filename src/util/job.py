""""
/*---------------------------------------------------------------------------
                                Jobs
 ---------------------------------------------------------------------------*/
"""
from util.event_logger import EventLogger

import Queue, threading

"""
/*---------------------------------------------------------------------------
                                AbstractJob
 ---------------------------------------------------------------------------*/
"""


class AbstractJob(threading.Thread):
    """
    The Job is the basis for all other jobs. Important is the updater parameter. Without it, the job wont start!
    Params:
    updater     =>  An Updater class object.
    Return:
    None
    Exceptions:
    None
    """

    def __init__(self, updater=None, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs,
                                  verbose=verbose)
        self._exit_flag = False
        self._job_name = "[JOB:" + self.name + "]"

        self._updater = updater

    def stop(self):
        self._exit_flag = True

    def _job(self):
        # check for needed objects
        if self._updater is None:
            return False;

        return True


"""
/*---------------------------------------------------------------------------
                                UpdateItemJob
 ---------------------------------------------------------------------------*/
"""


class UpdateItemJob(AbstractJob):
    """
    This Jobs starts the Item Update process.
    Params:
    updater     =>  An Updater(Item) class object.
    Return:
    None
    """
    def __init__(self, updater=None, group=None, name="UpdateItemJob", args=(), kwargs=None, verbose=None):
        target = self._job

        AbstractJob.__init__(self, updater=updater, group=group, target=target, name=name, args=args, kwargs=kwargs,
                             verbose=verbose)

    def _job(self):
        # check for needed objects
        if not AbstractJob._job(self):
            EventLogger.critical(str(self._job_name) + " stopped!!")
            return

        EventLogger.debug(str(self._job_name) + " updater=" + str(self._updater))
        ret_value = self._updater.start()
        EventLogger.debug(str(self._job_name) + " " + str(ret_value))


"""
/*---------------------------------------------------------------------------
                                UpdateRuleJob
 ---------------------------------------------------------------------------*/
"""


class UpdateRuleJob(AbstractJob):
    """
    This Jobs starts the Rule Update process.
    Params:
    updater     =>  An Updater(Rule) class object.
    Return:
    None
    """
    def __init__(self, updater=None, group=None, name="UpdateRuleJob", args=(), kwargs=None, verbose=None):
        target = self._job

        AbstractJob.__init__(self, updater=updater, group=group, target=target, name=name, args=args, kwargs=kwargs,
                             verbose=verbose)

    def _job(self):
        # check for needed objects
        if not AbstractJob._job(self):
            EventLogger.critical(str(self._job_name) + " stopped!!")
            return

        EventLogger.debug(str(self._job_name) + " updater=" + str(self._updater))
        ret_value = self._updater.start()
        EventLogger.debug(str(self._job_name) + " " + str(ret_value))

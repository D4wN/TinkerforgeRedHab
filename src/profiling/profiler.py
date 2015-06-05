import os
from src.util.event_logger import EventLogger


class Profiler():

    PROFILE_LOCATION_PATH = "./openHabProfiles"

    def __init__(self, name):
        self._name = name

    def startProfileRoutine(self, recognized_name):
        #1. look for profile
        #1.1 no profile found -> message to main
        #2. profile found -> new updater Thread
        #TODO start new thread with reading profile Data and doing shit
        pass

    def _debugShowProfileList(self):
        profile_dir = os.path.join(os.path.dirname(__file__), "..", "..", Profiler.PROFILE_LOCATION_PATH) #FIXME relative path?
        files = os.listdir(profile_dir)

        if files is None:
            EventLogger.debug(str(self._name) + " No Files Found!")
            return

        for f in files:
            print str(f)

    def __str__(self):
        return "Profiler-Object:[name:" + str(self._name) + "]"
import codecs
import os
from src.profiling.habUpdater import HabUpdater
from src.util.event_logger import EventLogger


class Profiler():
    PROFILE_LOCATION_PATH = "./openHabProfiles"

    def __init__(self, name):
        self._name = name

    def startProfileRoutine(self, recognized_name):
        EventLogger.debug(str(self._name) + " Profile Name: " + str(recognized_name))
        # 1. look for profile
        files = self.__getProfileList()
        if files is None:
            # 1.1 no profile found -> message to main
            EventLogger.info(str(self._name) + " No Profiles found in " + str(Profiler.PROFILE_LOCATION_PATH))
            return

        found = False
        for f in files:
            if str(f) == str(recognized_name) or str(f[:f.find(".")]) == str(recognized_name): #TODO find substring without .profile
                found = True
                # TODO do something more
                #2. profile found -> new updater Thread
                EventLogger.debug(str(self._name) + " Profile(" + str(recognized_name) + ") found!")

                path_to_file = os.path.join(os.path.dirname(__file__), "..", "..", Profiler.PROFILE_LOCATION_PATH, recognized_name+".profile")
                #EventLogger.debug(str(self._name) + "PATH: " + str(path_to_file))


                with codecs.open(path_to_file, 'r', 'UTF-8') as content_file:
                    HabUpdater("[Profiler:"+str(recognized_name)+"]", content_file)
                break;

        if not found:
            EventLogger.warning(str(self._name) + " Profile(" + str(recognized_name) + ") not found!")

    def __getProfileList(self):
        try:
            profile_dir = os.path.join(os.path.dirname(__file__), "..", "..",
                                       Profiler.PROFILE_LOCATION_PATH)  # FIXME relative path?
            files = os.listdir(profile_dir)
        except Exception as e:
            EventLogger.error(str(self._name) + ".__getProfileList: Exception(" + str(e) + ")")
            return None

        return files

    def _debugShowProfileList(self):
        files = self.__getProfileList()

        if files is None:
            EventLogger.debug(str(self._name) + " No Files Found!")
            return

        for f in files:
            print str(f)

    def __str__(self):
        return "Profiler-Object:[name:" + str(self._name) + "]"
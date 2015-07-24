import codecs
import os
from profiling.habUpdater import HabUpdater
from util.event_logger import EventLogger

"""
/*---------------------------------------------------------------------------
                                Profiler
 ---------------------------------------------------------------------------*/
"""
class Profiler():
    PROFILE_LOCATION_PATH = "./openHabProfiles"

    """
    Init of the class.
    Params:
    name        =>  Name of the Profiler, usually used for Debug purpose.
    """
    def __init__(self, name):
        self._name = name

    """
    Main function of this class. First checks for profile files, then if the given recognized_name exists
    and if it exists, it's contents will be read and given to the HubUpdater class.
    Params:
    recognized_name     =>  The name of the recognized person. Equals the profile file name.
    remove_mode         =>  Default: False. If set to True, the Rules of the profile will be removed from them openHab
                            rules file and the Items will be inverted, if possible(ON->OFF).
    Return:
    None
    """

    def start_profile_routine(self, recognized_name, remove_mode=False):
        EventLogger.debug(str(self._name) + " Profile Name: " + str(recognized_name))
        # 1. look for profile
        files = self.__get_profile_list()
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
                    HabUpdater(recognized_name, content_file, remove_mode)
                break;

        if not found:
            EventLogger.warning(str(self._name) + " Profile(" + str(recognized_name) + ") not found!")

    """
    This function will return a list of profile names in a specific folder(currently ../../openHabProfiles)
    Params:
    None
    Return:
    profile_list     =>  A list of profile names in a given folder.
    """

    def __get_profile_list(self):
        try:
            profile_dir = os.path.join(os.path.dirname(__file__), "..", "..",
                                       Profiler.PROFILE_LOCATION_PATH)  # FIXME relative path?
            files = os.listdir(profile_dir)
        except Exception as e:
            EventLogger.error(str(self._name) + ".__getProfileList: Exception(" + str(e) + ")")
            return None

        return files

    """
    Simple Debug function to print the profile list.
    Params:
    None
    Return:
    On Success      =>  Nothing
    On Error        =>  A Error Message
    """

    def _debug_show_profile_list(self):
        files = self.__get_profile_list()

        if files is None:
            EventLogger.debug(str(self._name) + " No Files Found!")
            return

        for f in files:
            print str(f)

    def __str__(self):
        return "Profiler-Object:[name:" + str(self._name) + "]"
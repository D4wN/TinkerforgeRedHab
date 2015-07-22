import json
from profiling.updater import RESTUpdater, RuleUpdater
from util.event_logger import EventLogger
from util.job import UpdateItemJob, UpdateRuleJob

"""
Comments TODO
"""


class HabUpdater():
    PROFILE_KEY_ITEMS = "items"
    PROFILE_KEY_RULES = "rules"
    PROFILE_KEY_ID = "id"
    # PROFILE_KEY_NAME = "name"

    def __init__(self, name, profile_file, remove_mode=False):
        self._name = "[Profiler:" + str(name) + "]"
        self._profile_name = name
        self._profile_file = profile_file
        self._profile_content = None;
        self._jobs = []
        self._remove_mode = remove_mode;

        if not self.__readProfile():
            EventLogger.critical(self._name + " Update Process stopped!")
            return
        self.__startJobs()

    def __readProfile(self):

        try:
            self._profile_content = json.load(self._profile_file)
        except ValueError as e:
            EventLogger.critical(str(self._name) + " Cant parse the configuration file: " + str(e))
            return False

        EventLogger.debug(self._name + " Loaded Profile: " + str(self._profile_content))
        return True

    def __startJobs(self):
        # ITEMS
        EventLogger.debug(self._name + " Items:")
        for key in self._profile_content[HabUpdater.PROFILE_KEY_ITEMS].keys():
            value = self._profile_content[HabUpdater.PROFILE_KEY_ITEMS][key]
            EventLogger.debug(self._name + " [" + str(key) + "]=" + str(value))

            # self._jobs.append(UpdateItemJob(updater=ItemUpdaterObject(key, value), name="UpdateItemJob["+str(key)+"]"))
            self._jobs.append(UpdateItemJob(updater=RESTUpdater(key, value, self._remove_mode),
                                            name="UpdateItemJob[" + str(key) + "]"))

        # RULES
        EventLogger.debug(self._name + " Rules:")
        try:
            self._jobs.append(UpdateRuleJob(updater=RuleUpdater(self._profile_content[HabUpdater.PROFILE_KEY_RULES],
                                                                self._profile_content[HabUpdater.PROFILE_KEY_ID],
                                                                self._profile_name,
                                                                self._remove_mode),
                                            name="UpdateRuleJob[" + str(self._profile_name) + "]"))
        except Exception as e:
            EventLogger.warning(self._name + " Rules Job could not be started! " + str(e))

        for j in self._jobs:
            j.start()
        for j in self._jobs:
            j.join()

        EventLogger.debug(str(self._name) + " All Jobs Done! Report to Main...")
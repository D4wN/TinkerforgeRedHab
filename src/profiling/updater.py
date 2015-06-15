from src.util.event_logger import EventLogger


class AbstractUpdaterObject():
    def __init__(self, key, value):
        self._key = key
        self._value = value

    def __str__(self):
        return "[Key:" + str(self._key) + ", Value:" + str(self._value) + "]"


class ItemUpdaterObject(AbstractUpdaterObject):
    def __init__(self, key, value):
        AbstractUpdaterObject.__init__(self, key, value)


""" old idea
class AbstractUpdater():
    def __init__(self, key, value):
        self._key = key
        self._value = value

    def startUpdating(self):
        if self._key is None:
            EventLogger.critical("Updater Key was None!")
            return False

        if self._value is None:
            EventLogger.critical("Updater Value was None!")
            return False

        return True


class RESTUpdater(AbstractUpdater):
    def __init__(self, key, value):
        AbstractUpdater.__init__(self, key, value)

    def startUpdating(self):
        if not AbstractUpdater.startUpdating(self):
            return
"""

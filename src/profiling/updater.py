import requests
from src.util.event_logger import EventLogger


class AbstractUpdaterObject():
    def __init__(self, key, value):
        self._key = key
        self._value = value

    def start(self):
        pass

    def __str__(self):
        return "[Key:" + str(self._key) + ", Value:" + str(self._value) + "]"


class ItemUpdaterObject(AbstractUpdaterObject):
    def __init__(self, key, value):
        AbstractUpdaterObject.__init__(self, key, value)


class RESTUpdater(AbstractUpdaterObject):
    OPENHAB_IP = "192.168.0.32:8080"

    def __init__(self, key, value):
        AbstractUpdaterObject.__init__(self, key, value)
        self._name = "[RESTUpdater:" + self._key + "," + self._value + "]"

    def start(self):
        #EventLogger.debug(self._name + " started...")
        try:
            return self.__postCommand()
        except Exception as ce:
            EventLogger.error(self._name + " " + str(ce))
            return self._name + " " + str(ce)

    def __postCommand(self):
        EventLogger.debug(self._name + " POST[key:" + self._key + "|value:" + self._value + "]")
        header = {'Content-Type': 'text/plain'}
        url = 'http://%s/rest/items/%s' % (RESTUpdater.OPENHAB_IP, self._key)
        #print "URL  :" + str(url)
        #print "DATA :" + str(self._value)

        req = requests.post(url, data=self._value, headers=header)
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        return "Status: " + str(requests.codes.ok)


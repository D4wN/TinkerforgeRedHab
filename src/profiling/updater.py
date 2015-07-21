import os
import requests
from util.event_logger import EventLogger


class AbstractUpdaterObject():
    def __init__(self, key, value):
        self._key = key
        self._value = value
        self._name = "[AbstractUpdaterObject:" + str(self._key) + "," + str(self._value) + "]"

    def start(self):
        EventLogger.warning(self.__str__() + " NYI!")

    def __str__(self):
        return str(self._name)


class ItemUpdaterObject(AbstractUpdaterObject):
    def __init__(self, key, value):
        AbstractUpdaterObject.__init__(self, key, value)
        self._name = "[ItemUpdaterObject:" + self._key + "," + self._value + "]"


class RESTUpdater(AbstractUpdaterObject):
    OPENHAB_IP = "192.168.0.32:8080"
    # TODO find better solution for inverting values, or resetting them
    KNOWN_VALUE_NEGATIVES = {
        'ON': 'OFF',
        'OFF': 'ON'
    }

    def __init__(self, key, value, reset_item=False):
        AbstractUpdaterObject.__init__(self, key, value)
        self._name = "[RESTUpdater:" + self._key + "," + self._value + "]"
        self._reset_item = reset_item

    def start(self):
        if self._reset_item:
            EventLogger.debug("In reset")
            if RESTUpdater.KNOWN_VALUE_NEGATIVES.has_key(self._value):
                EventLogger.debug("In invert")
                self._value = RESTUpdater.KNOWN_VALUE_NEGATIVES[self._value]
            else:
                EventLogger.warning(
                    self._name + " POST[key:" + self._key + "|value:" + self._value + "] Could not reset! No known invert value found!")
                return self._name + " No known invert value found! Item could not reset"

        # EventLogger.debug(self._name + " started...")
        try:
            return self.__postCommand()
        except Exception as ce:
            EventLogger.error(self._name + " " + str(ce))
            return self._name + " " + str(ce)

    def __postCommand(self):
        EventLogger.debug(self._name + " POST[key:" + self._key + "|value:" + self._value + "]")
        header = {'Content-Type': 'text/plain'}
        url = 'http://%s/rest/items/%s' % (RESTUpdater.OPENHAB_IP, self._key)
        # print "URL  :" + str(url)
        # print "DATA :" + str(self._value)

        req = requests.post(url, data=self._value, headers=header)
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        return "Status: " + str(requests.codes.ok)


class RuleUpdater(AbstractUpdaterObject):
    PATH_RULES_KEY = "PATH_TO_RULES_FILE"
    RULE_START_FORMATTER = "#start#%s#%s#"  # % (key, value)
    RULE_END_FORMATTER = "#end#%s#%s#"

    def __init__(self, rules, key=None, value=None, remove_rules=False):
        AbstractUpdaterObject.__init__(self, key, value)
        self._rules = rules
        self._name = "[RuleUpdater:" + str(self._key) + "," + str(self._value) + "]"
        self._remove_rules = remove_rules;

    def start(self):
        from profiling.habUpdater import HabUpdater
        EventLogger.debug(self._name + " started...")

        # check dir for ID entry
        if self._key is None:
            return self.__errorReturn(self._name + " No ID was specified in the Profile!")

        if not self._rules.has_key(RuleUpdater.PATH_RULES_KEY):
            return self.__errorReturn(self._name + " Rules have no entries \"" + RuleUpdater.PATH_RULES_KEY + "\"")

        # check if rules file exists

        if not os.path.isfile(self._rules[RuleUpdater.PATH_RULES_KEY]):
            return self.__errorReturn(
                self._name + " No rules file found under \"" + self._rules[RuleUpdater.PATH_RULES_KEY] + "\"")

        # open rules to read all of them
        content = None
        with open(self._rules[RuleUpdater.PATH_RULES_KEY], "r") as f:
            content = f.read()

        if content is None:
            return self.__errorReturn(self._name + " Content of the rules could not be read!")
        for rule in self._rules[HabUpdater.PROFILE_KEY_RULES]:

            if self._remove_rules:
                content = self._removeRule(content, rule)
            else:
                content = self._insertRule(content, rule)

        # write content back
        # FIXME: Permission Problems? How can we open the file as Admin?!
        with open(self._rules[RuleUpdater.PATH_RULES_KEY], "w") as f:
            f.write(content);

        return self._name + " Rules injected!"

    def _insertRule(self, content, rule):
        ##add identifier to the rule TODO: temp solution, need format?
        rule = (
            ("\n//#start#%s#%s#\n" % (self._key, self._value)) + rule + (
                "\n//#end#%s#%s#\n" % (self._key, self._value)))
        cleaned_rule = self.__cleanString(rule)
        cleaned_content = self.__cleanString(content)  # for simple contains search functionality

        if cleaned_rule not in cleaned_content:
            EventLogger.info(self._name + " Inserted Rule: " + cleaned_rule)
            content += str(rule)
        else:
            EventLogger.warning(self._name + " Rule already in rules File!")

        return content

    def _removeRule(self, content, rule):
        rule = (
            ("\n//#start#%s#%s#\n" % (self._key, self._value)) + rule + (
                "\n//#end#%s#%s#\n" % (self._key, self._value)))
        cleaned_rule = self.__cleanString(rule)
        cleaned_content = self.__cleanString(content)  # for simple contains search functionality

        if cleaned_rule in cleaned_content:
            EventLogger.info(self._name + " Removed Rule: " + cleaned_rule)
            content = content.replace(rule, '')  # TODO bettersolution to remove the rule?
        else:
            EventLogger.warning(self._name + " Rule not in rules File!")

        return content

    def __cleanString(self, s):
        return s.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')

    def __errorReturn(self, msg):
        EventLogger.error(msg)
        return msg
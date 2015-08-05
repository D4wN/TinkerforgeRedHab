import os
import requests
from util.event_logger import EventLogger

"""
/*---------------------------------------------------------------------------
                                AbstractUpdaterObject
 ---------------------------------------------------------------------------*/
"""


class AbstractUpdaterObject():
    def __init__(self, key, value):
        self._key = key
        self._value = value
        self._name = "[AbstractUpdaterObject:" + str(self._key) + "," + str(self._value) + "]"

    def start(self):
        EventLogger.warning(self.__str__() + " NYI!")

    def __str__(self):
        return str(self._name)


"""
/*---------------------------------------------------------------------------
                                ItemUpdaterObject
 ---------------------------------------------------------------------------*/
"""


class ItemUpdaterObject(AbstractUpdaterObject):
    """
    NYI
    """

    def __init__(self, key, value):
        AbstractUpdaterObject.__init__(self, key, value)
        self._name = "[ItemUpdaterObject:" + str(self._key) + "," + str(self._value) + "]"


"""
/*---------------------------------------------------------------------------
                                RESTUpdater
 ---------------------------------------------------------------------------*/
"""


class RESTUpdater(AbstractUpdaterObject):
    # OPENHAB_IP = "192.168.0.32:8080"  # FIXME should be in the profile file?
    OPENHAB_IP = "localhost:8080"  # FIXME DEMO URL ONLY!
    # TODO find better solution for inverting values, or resetting them
    KNOWN_VALUE_NEGATIVES = {
        'ON': 'OFF',
        'OFF': 'ON',
        'TFNUM<00>Hallo: Marvin': 'TFNUM<00>Wiedersehen! '  # TODO Temp only to delte the message
    }

    """
    This class updates Items values over the REST Api.
    Params:
    key             =>  Item name/description.
    value           =>  The new value of the item.
    reset_item      =>  Default: False; If True, the item value will be inverted, if possible!
    Return:
    None
    """

    def __init__(self, key, value, reset_item=False):
        AbstractUpdaterObject.__init__(self, key, value)
        self._name = "[RESTUpdater:" + str(self._key) + "," + str(self._value) + "]"
        self._reset_item = reset_item

    def start(self):
        if self._reset_item:
            if RESTUpdater.KNOWN_VALUE_NEGATIVES.has_key(self._value):
                self._value = RESTUpdater.KNOWN_VALUE_NEGATIVES[self._value]
            else:
                EventLogger.warning(
                    self._name + " POST[key:" + str(self._key) + "|value:" + str(
                        self._value) + "] Could not reset! No known invert value found!")
                return self._name + " No known invert value found! Item could not reset"

        # EventLogger.debug(self._name + " started...")
        try:
            return self.__post_command()
        except Exception as ce:
            # EventLogger.error(self._name + " " + str(ce))
            EventLogger.warning(
                "Update Item[" + str(self._key) + "] with Value[" + str(
                    self._value) + "] was NOT successful! Error: " + str(
                    ce))
            return self._name + " " + str(ce)

    def __post_command(self):
        EventLogger.debug(self._name + " POST[key:" + str(self._key) + "|value:" + str(self._value) + "]")
        header = {'Content-Type': 'text/plain'}
        url = 'http://%s/rest/items/%s' % (RESTUpdater.OPENHAB_IP, str(self._key))
        # print "URL  :" + str(url)
        # print "DATA :" + str(self._value)

        req = requests.post(url, data=self._value, headers=header)
        if req.status_code != requests.codes.ok:
            req.raise_for_status()

        EventLogger.info("Update Item[" + str(self._key) + "] with Value[" + str(self._value) + "] was successful!")
        return "Status: " + str(requests.codes.ok)


"""
/*---------------------------------------------------------------------------
                                RuleUpdater
 ---------------------------------------------------------------------------*/
"""


class RuleUpdater(AbstractUpdaterObject):
    PATH_RULES_KEY = "PATH_TO_RULES_FILE"
    RULE_START_FORMATTER = "#start#%s#%s#"  # % (key, value)
    RULE_END_FORMATTER = "#end#%s#%s#"

    """
    This class updates the rules file of openHab. ONLY working on localhost right now!
    Params:
    rules           =>  The rules as list.
    key             =>  ID of the profile.
    value           =>  Name of the profile.
    remove_rules    =>  Default: False; If True, rules will be removed from the rules file, if possible!
    Return:
    None
    """

    def __init__(self, rules, key=None, value=None, remove_rules=False):
        AbstractUpdaterObject.__init__(self, key, value)
        self._rules = rules
        self._name = "[RuleUpdater:" + str(self._key) + "," + str(self._value) + "]"
        self._remove_rules = remove_rules;

    """
    This function starts the rule update process.
    Params:
    None
    Return:
    On Success      =>  Message(Rules injected!)
    On Error        =>  Error message.
    """

    def start(self):
        from profiling.habUpdater import HabUpdater

        EventLogger.debug(self._name + " started...")

        # check dir for ID entry
        if self._key is None:
            return self.__error_return(self._name + " No ID was specified in the Profile!")

        if not self._rules.has_key(RuleUpdater.PATH_RULES_KEY):
            return self.__error_return(self._name + " Rules have no entries \"" + RuleUpdater.PATH_RULES_KEY + "\"")

        # check if rules file exists

        if not os.path.isfile(self._rules[RuleUpdater.PATH_RULES_KEY]):
            return self.__error_return(
                self._name + " No rules file found under \"" + self._rules[RuleUpdater.PATH_RULES_KEY] + "\"")

        # open rules to read all of them
        content = None
        with open(self._rules[RuleUpdater.PATH_RULES_KEY], "r") as f:
            content = f.read()

        if content is None:
            return self.__error_return(self._name + " Content of the rules could not be read!")
        for rule in self._rules[HabUpdater.PROFILE_KEY_RULES]:

            if self._remove_rules:
                content = self._remove_rule(content, rule)
            else:
                content = self._insert_rule(content, rule)

        # write content back
        # FIXME: Permission Problems? How can we open the file as Admin?!
        with open(self._rules[RuleUpdater.PATH_RULES_KEY], "w") as f:
            f.write(content);

        return self._name + " Rules updated!"

    """
    This function injects a rule into the rules file.
    Params:
    content         =>  The current rules file content as string.
    rule            =>  The rule as string.
    Return:
    content         =>  The new content as string.
    """

    def _insert_rule(self, content, rule):
        ##add identifier to the rule TODO: temp solution, need format?
        rule = (
            ("\n//#start#%s#%s#\n" % (self._key, self._value)) + rule + (
                "\n//#end#%s#%s#\n" % (self._key, self._value)))
        cleaned_rule = self.__clean_string(rule)
        cleaned_content = self.__clean_string(content)  # for simple contains search functionality

        if cleaned_rule not in cleaned_content:
            EventLogger.info(" Inserted Rule: " + cleaned_rule)
            content += str(rule)
        else:
            EventLogger.warning("Rule already in rules File! [" + str(self.__get_rule_name(rule)) + "]")

        return content

    """
    This function removes a rule from the rules file.
    Params:
    content         =>  The current rules file content as string.
    rule            =>  The rule as string.
    Return:
    content         =>  The new content as string.
    """

    def _remove_rule(self, content, rule):
        rule = (
            ("\n//#start#%s#%s#\n" % (self._key, self._value)) + rule + (
                "\n//#end#%s#%s#\n" % (self._key, self._value)))
        cleaned_rule = self.__clean_string(rule)
        cleaned_content = self.__clean_string(content)  # for simple contains search functionality

        if cleaned_rule in cleaned_content:
            EventLogger.info("Removed Rule: " + cleaned_rule)
            content = content.replace(rule, '')  # TODO bettersolution to remove the rule?
        else:
            EventLogger.warning("Rule not in rules File! [" + str(self.__get_rule_name(rule)) + "]")

        return content

    """
    This function injects a rule into the rules file.
    Params:
    s           =>  A String which will be cleaned.
    Return:
    s           =>  The cleaned String.
    """

    def __clean_string(self, s):
        return s.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')

    def __get_rule_name(self, rule):
        try:
            start = rule.index("rule")
            mid = rule.index("\"", start + 1)  # first "
            end = rule.index("\"", mid + 1) + 1  # second "
            # EventLogger.debug("__get_rule_name Start("+str(start)+") Mid("+str(mid)+") End("+str(end)+")")
            rule = rule[start:end]
        except ValueError as ve:
            EventLogger.warning(self._name + " __get_rule_name(...) ValueError: " + str(ve))

        return rule

    """
    A Function to log and return an Error.
    Params:
    msg         =>  The Error message.
    Return:
    msg         =>  The Error message.
    """

    def __error_return(self, msg):
        EventLogger.error(msg)
        return msg
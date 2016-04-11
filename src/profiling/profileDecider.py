from util.event_logger import EventLogger
from util.ringbuffer import RingBuffer

class ProfileDecider:
    CALLBACK_BUFFER_SIZE = 5
    CALLBACK_BUFFER = RingBuffer(CALLBACK_BUFFER_SIZE)

    # E.g. Profile some(10) need fewer then 7(Threshold 10 - Threshold_Percentage 10*0,3) faces to revert back to few(5)
    PROFILE_THRESHOLD_PERCENTAGE = 0.3
    # Profile names and threshold values # TODO change algo for percentage detection? look at space between profile and next lowest instead of the profile value
    PROFILE_THRESHOLD = {
        'few': 5,
        'some': 10,
        'many': 20
    }
    CURRENT_ACTIVE_PROFILE = None

    def __init__(self):
        self._name = "[ProfileDecider]"

    def decide(self, cb):
        EventLogger.info(self._name + " started.")
        EventLogger.info(self._name + " Current active Profile = " + str(ProfileDecider.CURRENT_ACTIVE_PROFILE))
        if cb is None:
            EventLogger.error(self._name + " decide did not get a callback!")
            return

        buf = ProfileDecider.CALLBACK_BUFFER.get()
        # print buf

        median = self._create_median(buf)
        profile_name = self._check_threshold(median)

        EventLogger.debug(self._name + " NewProfile: " + str(profile_name) + ", Median = " + str(median))
        # print "Name = " + str(profile_name) + ", Median = " + str(median)

        cb(profile_name)

    def _check_threshold(self, median):
        last = "few"  # default value
        for profile_name in ProfileDecider.PROFILE_THRESHOLD:
            profile_value = ProfileDecider.PROFILE_THRESHOLD[profile_name]
            # print profile_name, profile_value
            if median < profile_value:
                break
            last = profile_name

        # no active profile yet, use the new profile
        if ProfileDecider.CURRENT_ACTIVE_PROFILE is None:
            return last

        # active profile, but is lower than new profile
        if ProfileDecider.PROFILE_THRESHOLD[ProfileDecider.CURRENT_ACTIVE_PROFILE] < ProfileDecider.PROFILE_THRESHOLD[
            last]:
            EventLogger.debug(self._name + " HIGH_CHECK: active=" + str(
                ProfileDecider.PROFILE_THRESHOLD[ProfileDecider.CURRENT_ACTIVE_PROFILE]) + " last=" + str(
                ProfileDecider.PROFILE_THRESHOLD[last]))
            return last

        # new profile lower then active profile -> look at threshold_percentage
        act_v = ProfileDecider.PROFILE_THRESHOLD[ProfileDecider.CURRENT_ACTIVE_PROFILE]
        new_v = ProfileDecider.PROFILE_THRESHOLD[last]
        thres_p = act_v - act_v * ProfileDecider.PROFILE_THRESHOLD_PERCENTAGE
        EventLogger.debug(
            self._name + " LOWER_CHECK: act_v=" + str(act_v) + " new_v=" + str(new_v) + " thres_p=" + str(thres_p))

        # return new profile name, if threshold_percentage is reached
        if median <= thres_p:
            # check if nothing changed
            if ProfileDecider.CURRENT_ACTIVE_PROFILE == last:
                return None
            return last

        # return no change
        return None

    def _create_median(self, buf):
        sum = 0;
        for data in buf:
            sum += data.x
            # print str(data.x) + "+"
        return (sum / len(buf))

class FaceCounterData:
    def __init__(self, tv_module_id, x, y, height, width, msg):
        self.tv_module_id = tv_module_id
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.msg = msg

    def __str__(self):
        tmp_msg = self.msg
        if self.msg is None or self.msg == "":
            tmp_msg = "No Message"
        return "(" + str(self.tv_module_id) + "|" + str(self.x) + "|" + str(self.y) + "|" + str(
            self.height) + "|" + str(self.width) + "|" + str(tmp_msg) + ")"

    def __repr__(self):
        return self.__str__()

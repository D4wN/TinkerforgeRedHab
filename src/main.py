import sys
from recognition.recognition_runner import RecognitionRunner
from recognition.recognizer import FaceRecognizer, NfcRfidRecognizer

# print sys.path

from profiling.profiler import Profiler
from util.event_logger import EventLogger, ConsoleLogger


def __init_event_logging():
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    #EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))



if __name__ == "__main__":
    runner = RecognitionRunner(NfcRfidRecognizer())
    runner.start()

"""
    name = "Marvin Lutz"
    print name
    arr = Utils.string_to_byte_array(name)
    print str(arr)
    new_name = Utils.byte_array_to_string(arr)
    print new_name

    nfc()"""
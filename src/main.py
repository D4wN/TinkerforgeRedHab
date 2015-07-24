import sys

print sys.path

from profiling.profiler import Profiler
from util.event_logger import EventLogger, ConsoleLogger

def __init_event_logging():
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    #EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))

if __name__ == '__main__':
    __init_event_logging()

    p = Profiler("[Profiler:Main]")
    # p._debug_show_profile_list()
    # p.startProfileRoutine("test", True)
    p.start_profile_routine("test", False)

    #1. Start Recognition(THREAD)
    #2. Wait for Answers -> (Recognized Person)
    #3. Profiling(THREAD)
    #4. Wait for Answers -> (Profile Update Status)
    #??? Profit
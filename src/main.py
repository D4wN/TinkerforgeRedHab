from src.profiling.profiler import Profiler
from src.util.event_logger import EventLogger, FileLogger, ConsoleLogger

def __init_event_logging():
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    #EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))

if __name__ == '__main__':
    __init_event_logging()

    p = Profiler("[Profiler:Main]");
    #p._debugShowProfileList()
    p.startProfileRoutine("test");

    #1. Start Recognition(THREAD)
    #2. Wait for Answers -> (Recognized Person)
    #3. Profiling(THREAD)
    #4. Wait for Answers -> (Profile Update Status)
    #??? Profit
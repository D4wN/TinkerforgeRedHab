import sys
from recognition.recognition_runner import RecognitionRunner
from recognition.recognizer import FaceRecognizer, NfcRfidRecognizer, FaceCountRecognizer

# print sys.path

from util.event_logger import EventLogger, ConsoleLogger, FileLogger


def __init_event_logging():
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))


if __name__ == "__main__":
    __init_event_logging()

    EventLogger.debug( "\nargv[1] == FaceCounter => FaceCounter")

    if len(sys.argv) < 2:
        EventLogger.error("Aborting Program, wrong Parameters!")

    elif sys.argv[1] == "DEBUG":
        EventLogger.info("DEBUG MODE STAERTED...")
        # Here the Runner with Debug mode
        # runner = RecognitionRunner(FaceRecognizer())
        runner = RecognitionRunner(FaceCountRecognizer())
        runner._start_debug()

    elif sys.argv[1].lower() == "facecounter":
        runner = RecognitionRunner(FaceCountRecognizer())
        runner.start()
    # elif sys.argv[1] == "0":
    #     EventLogger.debug("argv[1] == 0")
    #     EventLogger.info("NFC/RFID Writer")
    #     runner = RecognitionRunner(NfcRfidRecognizer())
    #     if len(sys.argv) >= 3:
    #         name = str(sys.argv[2])
    #         runner.start([name])
    #     else:
    #         EventLogger.debug("argv[2] == ??? Missing name! Aborting Program")
    #
    # elif sys.argv[1] == "1":
    #     EventLogger.debug("len(argv) == 1")
    #     EventLogger.info("NFC/RFID Recognition")
    #     runner = RecognitionRunner(NfcRfidRecognizer())
    #     runner.start()
    #
    # elif sys.argv[1] == "2":
    #     EventLogger.debug("argv[1] == 2")
    #     EventLogger.info("Face Recognition")
    #     runner = RecognitionRunner(FaceRecognizer())
    #     runner.start([None, 2])

    else:
        EventLogger.debug("argv[1] == " + str(sys.argv[1]))
        EventLogger.error("Aborting Program, wrong Parameters!")

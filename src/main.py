import sys
from recognition.recognition_runner import RecognitionRunner
from recognition.recognizer import FaceRecognizer, NfcRfidRecognizer

# print sys.path

from util.event_logger import EventLogger, ConsoleLogger


def __init_event_logging():
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    #EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))


if __name__ == "__main__":
    __init_event_logging()
    EventLogger.debug(
        "\nargv[1] == 0 => NFC/RFID Writing argv[2] = name\nargv[1] == 1 => NFC/RFID Recognition\nargv[1] == 2 => Face Recognition")

    if len(sys.argv) < 2:
        EventLogger.error("Aborting Program, wrong Parameters!")

    elif sys.argv[1] == "0":
        EventLogger.debug("argv[1] == 0")
        EventLogger.info("NFC/RFID Writer")
        runner = RecognitionRunner(NfcRfidRecognizer())
        if len(sys.argv) >= 3:
            name = str(sys.argv[2])
            runner.start([name])
        else:
            EventLogger.debug("argv[2] == ??? Missing name! Aborting Program")

    elif sys.argv[1] == "1":
        EventLogger.debug("len(argv) == 1")
        EventLogger.info("NFC/RFID Recognition")
        runner = RecognitionRunner(NfcRfidRecognizer())
        runner.start()

    elif sys.argv[1] == "2":
        EventLogger.debug("argv[1] == 2")
        EventLogger.info("Face Recognition")
        runner = RecognitionRunner(FaceRecognizer())
        runner.start([None, 2])

    else:
        EventLogger.debug("argv[1] == " + str(sys.argv[1]))
        EventLogger.error("Aborting Program, wrong Parameters!")

import sys
from recognition.recognition_runner import RecognitionRunner
from recognition.recognizer import FaceRecognizer, NfcRfidRecognizer

# print sys.path

from profiling.profiler import Profiler
from util.event_logger import EventLogger, ConsoleLogger
from util.utils import Utils


def __init_event_logging():
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    #EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))


def nfc():
    print "NFC STARTED"
    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.bricklet_nfc_rfid import NFCRFID

    HOST = "localhost"
    PORT = 4223
    UID = "oDg"  # Change to your UID

    ipcon = IPConnection()  # Create IP connection
    nr = NFCRFID(UID, ipcon)  # Create device object

    ipcon.connect(HOST, PORT)  # Connect to brickd
    # Don't use device before ipcon is connected

    # Register state changed callback to function cb_state_changed
    nr.register_callback(nr.CALLBACK_STATE_CHANGED,
                         lambda x, y: cb_state_changed(x, y, nr))

    # Select NFC Forum Type 2 tag
    nr.request_tag_id(nr.TAG_TYPE_TYPE2)

    raw_input('Press key to exit\n')  # Use input() in Python 3
    nr.request_tag_id(nr.TAG_TYPE_TYPE2)

    raw_input('Press key2 to exit\n')  # Use input() in Python 3

    ipcon.disconnect()


# Callback function for state changed callback
def cb_state_changed(state, idle, nr):
    if state == nr.STATE_REQUEST_TAG_ID_READY:
        print('Tag found')

        # Write 16 byte to pages 5-8
        # 16 buchstaben

        data_write = Utils.string_to_byte_array("Marvin Lutz")
        nr.write_page(5, data_write)
        print('Writing data...')

    elif state == nr.STATE_WRITE_PAGE_READY:
        # Request pages 5-8
        nr.request_page(5)
        print('Requesting data...')

    elif state == nr.STATE_REQUEST_PAGE_READY:
        # Get and print pages
        data = nr.get_page()
        print 'Read data:' + str(Utils.byte_array_to_string(data))
        # print('Read data: [' + ' '.join(map(str, data)) + ']')

    elif state & (1 << 6):
        # All errors have bit 6 set
        print('Error: ' + str(state))


if __name__ == "__main__":
    #runner = RecognitionRunner(NfcRfidRecognizer())
    #runner.start(None)

    runner = RecognitionRunner(FaceRecognizer())
    runner.start([None, 2])

"""
    name = "Marvin Lutz"
    print name
    arr = Utils.string_to_byte_array(name)
    print str(arr)
    new_name = Utils.byte_array_to_string(arr)
    print new_name

    nfc()"""
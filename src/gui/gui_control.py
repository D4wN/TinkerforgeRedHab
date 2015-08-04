from tinkerforge.bricklet_dual_button import DualButton
from tinkerforge.bricklet_nfc_rfid import NFCRFID
from tinkerforge.ip_connection import IPConnection
from util.event_logger import EventLogger
from util.singleton import Singleton
from util.utils import Utils

"""
/*---------------------------------------------------------------------------
                                GuiControl
 ---------------------------------------------------------------------------*/
"""


@Singleton
class GuiControl():
    def __init__(self):
        self._name = "[GuiControl]"

        # ipcon
        self._ipcon = None
        self._HOST = "localhost"
        self._PORT = 4223

        #DualButton States
        self._db = None
        self._DB_UID = "mAo"
        self.recognition_running = True
        self.recognition_state = False
        #TODO bad idea?
        self.recognition_progress = False

        # NFC/RFID
        self._nfc = None
        self._NFC_UID = "oDg"
        self._nfc_cb_to_profiler = None
        self._nfc_write_mode = False
        self._nfc_write_name = None


    def start_ipcon(self):
        if self._ipcon != None:
            EventLogger.warning(self.name + " tried to start IPCON, but IPCON was already started!")
            return

        self._ipcon = IPConnection()

        # Init Components
        self._db = DualButton(self._DB_UID, self._ipcon)
        self._nfc = NFCRFID(self._NFC_UID, self._ipcon)

        try:
            self._ipcon.connect(self._HOST, self._PORT)
        except Exception as e:
            EventLogger.critical("A critical error occur: " + str(e))
            raise Exception("A critical error occur: " + str(e))

        #Init Callbacks
        self._db.register_callback(DualButton.CALLBACK_STATE_CHANGED, self.__cb_db_state_changed)
        self._nfc.register_callback(self._nfc.CALLBACK_STATE_CHANGED,
                                    lambda x, y: self.__cb_nfc_state_changed(x, y, self._nfc))

    def stop_ipcon(self):
        if self._ipcon == None:
            EventLogger.warning(self.name + " tried to disconnect IPCON, but IPCON was not connected!")
            return
        self._ipcon.disconnect()
        self._ipcon = None


    # DualButton Functions
    def __cb_db_state_changed(self, button_l, button_r, led_r, led_l):
        #Button Right = Programm Control => True = Program Quit
        if button_r == DualButton.BUTTON_STATE_PRESSED:
            led_r = DualButton.LED_STATE_OFF
            self._db.set_selected_led_state(DualButton.LED_RIGHT, led_r)
            # exit program
            self.recognition_running = False

        if not self.recognition_progress:
            if button_l == DualButton.BUTTON_STATE_PRESSED:
                led_l = DualButton.LED_STATE_ON
                self._db.set_selected_led_state(DualButton.LED_LEFT, led_l)
                self.recognition_state = True
            else:
                led_l = DualButton.LED_STATE_OFF
                self._db.set_selected_led_state(DualButton.LED_LEFT, led_l)
                self.recognition_state = False

    def _db_start_state(self):
        self._db.set_selected_led_state(DualButton.LED_LEFT, DualButton.LED_STATE_OFF)
        self._db.set_selected_led_state(DualButton.LED_RIGHT, DualButton.LED_STATE_ON)

    def _db_end_state(self):
        self._db.set_selected_led_state(DualButton.LED_LEFT, DualButton.LED_STATE_OFF)
        self._db.set_selected_led_state(DualButton.LED_RIGHT, DualButton.LED_STATE_OFF)

    def _db_recognizer_state_off(self):
        self._db.set_selected_led_state(DualButton.LED_LEFT, DualButton.LED_STATE_OFF)
        self.recognition_state = False
        self.recognition_progress = False

    def __cb_nfc_state_changed(self, state, idle, nr):
        name = "NO NAME"

        if state == nr.STATE_REQUEST_TAG_ID_READY:
            EventLogger.debug('Tag found')

            # Write 16 byte to pages 5-8
            if self._nfc_write_mode:
                data_write = Utils.string_to_byte_array(self._nfc_write_name)
                nr.write_page(5, data_write)
                EventLogger.debug('Writing data...')
            else:
                print "else mode"
                state = nr.STATE_WRITE_PAGE_READY  # FIXME baaad workaround!


        elif state == nr.STATE_WRITE_PAGE_READY:  # only when writing before!
            # Request pages 5-8
            nr.request_page(5)
            EventLogger.debug('Requesting data...')

        elif state == nr.STATE_REQUEST_PAGE_READY:
            # Get and print pages
            data = nr.get_page()
            name = str(Utils.byte_array_to_string(data))
            EventLogger.debug('Read data:' + name)

            if self._nfc_cb_to_profiler != None:
                self._nfc_cb_to_profiler(name)

        elif state & (1 << 6):
            # All errors have bit 6 set
            if state == self._nfc.STATE_REQUEST_TAG_ID_ERROR:
                EventLogger.info(
                    'No NFC/RFID Tag found! TODO: Message - Token @ Lesegereat -> Button')  # TODO: Message - Token @ Lesegeraet -> Button
            else:
                EventLogger.debug('Error: ' + str(state))

                # TODO check for errors in coding!
                #EventLogger.error(self._name + "_nfc_cb_to_profiler was None! DEBUG ONLY!")

    def _debug_print(self):
        print "self.recognition_running  = " + str(self.recognition_running) + "\nself.recognition_state    = " + str(
            self.recognition_state) + "\nself.recognition_progress = " + str(self.recognition_progress) + "\n"

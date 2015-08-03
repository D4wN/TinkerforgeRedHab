from tinkerforge.bricklet_dual_button import DualButton
from tinkerforge.ip_connection import IPConnection
from util.event_logger import EventLogger
from util.singleton import Singleton

"""
/*---------------------------------------------------------------------------
                                GuiControl
 ---------------------------------------------------------------------------*/
"""


@Singleton
class GuiControl():
    def __init__(self):
        self._name = "[GuiControl]"

        print "GuiController TODO"
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


    def start_ipcon(self):
        if self._ipcon != None:
            EventLogger.warning(self.name + " tried to start IPCON, but IPCON was already started!")
            return

        self._ipcon = IPConnection()

        # Init Components
        self._db = DualButton(self._DB_UID, self._ipcon)

        try:
            self._ipcon.connect(self._HOST, self._PORT)
        except Exception as e:
            EventLogger.critical("A critical error occur: " + str(e))
            raise Exception("A critical error occur: " + str(e))

        #Init Callbacks
        self._db.register_callback(DualButton.CALLBACK_STATE_CHANGED, self.__cb_db_state_changed)

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

    def _debug_print(self):
        print "self.recognition_running  = " + str(self.recognition_running) + "\nself.recognition_state    = " + str(
            self.recognition_state) + "\nself.recognition_progress = " + str(self.recognition_progress) + "\n"

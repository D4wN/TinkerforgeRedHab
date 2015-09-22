from thread import start_new_thread
from flask_webserver import FlaskWebserver
from gui.gui_control import GuiControl
from util.event_logger import EventLogger

"""
/*---------------------------------------------------------------------------
                                RecognitionRunner
 ---------------------------------------------------------------------------*/
"""


class RecognitionRunner():
    def __init__(self, recognizer):
        self._name = "[RecognitionRunner]"

        self._webserver = FlaskWebserver()


        self._gui = GuiControl.Instance()
        self._recognizer = recognizer

        self._gui.start_ipcon()

    def start(self, args=None):
        EventLogger.debug(self._name + " started running...")
        self._webserver.start()

        if self._recognizer == None:
            EventLogger.error(self._name + " has no Recognizer! Start aborted!")
            return

        # init DualButton LEDs
        self._gui._db_start_state()

        #0|1
        while self._gui.recognition_running:

            if not self._gui.recognition_progress and self._gui.recognition_state:
                #1|1
                self._gui.recognition_progress = True
                start_new_thread(self._recognizer.recognize, (self.__cb, args))

        #End
        EventLogger.debug(self._name + " stopped running...")

        #Wait for Webserver
        self._webserver.stop()
        self._webserver.join()

        self._gui._db_end_state()
        self._gui.stop_ipcon()

    def _start_debug(self, args=None):
        EventLogger.debug(self._name + " <DEBUG MODE> started running...")
        if self._recognizer == None:
            EventLogger.error(self._name + " has no Recognizer! Start aborted!")
            return

        # init DualButton LEDs
        self._gui._db_start_state()

        # 0|1
        while True:

            quit = raw_input('Type somtehing to start the Recognition, or "q" to end the Program:')
            if quit == "q":
                break

            self._gui.recognition_progress = True
            start_new_thread(self._recognizer.recognize, (self.__cb, args))


        #End
        EventLogger.debug(self._name + " stopped running...")

    def __cb(self, args):
        self._recognizer.cb_recognize(args)
        self._gui._db_recognizer_state_off()


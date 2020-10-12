from PyQt5 import QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QThreadPool

from GUI.mainWindow import Ui_MainWindow
from controller.controllerDate import ControllerDate

from tools.qtThreading import Worker


class ViewDate:

    def __init__(self, ui: Ui_MainWindow, controller: ControllerDate):
        # Set up UI and thread pool
        self.ui = ui
        self.controller = controller
        self.thread_pool = QThreadPool()

        # Register number of times the software try to reconnect if it lose the connection to a database
        self.try_to_reconnect = 0

        # Connect widgets to function
        self.__connect_date()
        self.__connect_spinbox()
        self.__connect_checkbox()

        # Call for setting date and ID
        self.__set_date()
        self.__set_id()

    def __del__(self):
        """
        Ensure the thread is stopped when deleting the view.
        """

        self.controller.automatic_thread_running = False

    def __connect_date(self):
        """
        Set date time to system local.
        Allow calendar to pop up if needed.
        """

        self.ui.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit.dateTimeChanged.connect(lambda: self.__set_date())

    def __connect_spinbox(self):
        self.ui.spinBox_id.valueChanged.connect(lambda: self.__set_id())

    def __connect_checkbox(self):
        self.ui.checkBox.stateChanged.connect(lambda: self.__connect_to_database())

    def __connect_to_database(self):
        """
        Call when automatic mode is enabled.
        """

        if self.ui.checkBox.isChecked():
            # Increment the reconnection try
            self.try_to_reconnect += 1

            # If we tried less than 50 times to connect to database, try again (with recursion).
            # Else, stop it and notify the user by unchecking the automatic box.
            if self.try_to_reconnect < 50:
                func = self.__connect_to_database
            else:
                func = lambda: self.ui.checkBox.setChecked(False)

            # Launch the thread. Connect update and finish function.
            self.controller.automatic_thread_running = True
            automatic_thread = Worker(self.controller.connect_to_most_recent_database, update_callback=True)
            automatic_thread.signals.update.connect(self.__update)
            automatic_thread.signals.finished.connect(func)
            self.thread_pool.start(automatic_thread)

            # Manual mode is disabled.
            self.ui.dateEdit.setEnabled(False)
            self.ui.spinBox_id.setEnabled(False)

        else:
            # End of automatic mode : manual mode enabled.
            self.try_to_reconnect = 0
            self.ui.dateEdit.setEnabled(True)
            self.ui.spinBox_id.setEnabled(True)
            self.controller.automatic_thread_running = False

    def __set_date(self):
        """
        Set date, ask for controller to search for corresponding image and database.
        Emit image_found if image and database are found, clear_image on the contrary.
        """

        date = self.ui.dateEdit.date()
        self.controller.set_date(date.day(), date.month(), date.year())
        if self.controller.check_directory_and_image():
            self.controller.model.image_found.emit()
            if self.controller.connect_to_database():
                self.controller.retrieve_conformity()
                self.controller.disconnect()
        else:
            self.controller.model.clear_image.emit()
            self.controller.model.display_status_msg.emit('Can\'t found an image corresponding to this date or Id')

    def __set_id(self):
        """
        Set id, ask for controller to search for corresponding image and database.
        Emit image_found if image and database are found, clear_image on the contrary.
        """

        self.controller.set_id(self.ui.spinBox_id.value())
        if self.controller.check_directory_and_image():
            self.controller.model.image_found.emit()
            if self.controller.connect_to_database():
                self.controller.retrieve_conformity()
                self.controller.disconnect()
        else:
            self.controller.model.clear_image.emit()
            self.controller.model.display_status_msg.emit('Can\'t find an image corresponding to this date or Id')

    def __update(self):
        """
        Called by the automatic mode thread.
        Update UI with found date / id.
        """

        date = QDate(self.controller.model.year,
                     self.controller.model.month + 1,
                     self.controller.model.day)
        self.ui.dateEdit.setDate(date)

        self.ui.spinBox_id.setValue(self.controller.model.id)

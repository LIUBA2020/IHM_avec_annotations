from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import sqlite3


class ImageDisplay(QtCore.QObject):
    # Images path has been found !
    image_found = pyqtSignal()
    # Clear image display
    clear_image = pyqtSignal()
    # Set text on the status label
    display_status_msg = pyqtSignal(str)

    def __init__(self):
        super(ImageDisplay, self).__init__()

        # Register date / id
        self.day = None
        self.month = None
        self.month_short_name = None
        self.year = None
        self.id = None

        # Register found directory and image path
        self.dir = None
        self.img = None

        # Register database stuff
        self.database_path = None
        self.database_connection = None
        self.database_cursor = None
        self.database_table = None

    def connect_to_database(self):
        """
        Try to connect to database with self.database_path
        :return: True if connection is OK, False if it is not
        """

        if self.database_path is not None:
            try:
                self.database_connection = sqlite3.connect(self.database_path)
                self.database_cursor = self.database_connection.cursor()
                return True
            except:
                return False

    def disconnect_from_database(self):
        """
        If a connection to a database is established, disconnect
        """

        if self.database_connection is not None:
            self.database_connection.close()
            self.database_connection = None
            self.database_cursor = None

    def choose_table(self, index: int=0):
        """
        Select every table in the database, make a list out of it and register the table corresponding to the index.
        :param index: int, default : 0
        """

        self.database_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.database_cursor.fetchone()

        self.database_table = tables[index]

    def retrieve_conformity_from_id(self, id: int):
        """
        Check for the conformity state corresponding to the id
        :param id: int
        :return: conformity state (0 or 1) or None is nothing is found
        """

        if self.database_cursor is not None and self.database_table is not None:
            cmd = "SELECT conformity FROM {0} WHERE id={1}".format(self.database_table, id)
            self.database_cursor.execute(cmd)
            return self.database_cursor.fetchone()[0]
        else:
            return None

    def retrieve_last_entry(self):
        """
        Retrieve last entry id in current database
        :return: id corresponding to last entry
        """

        if self.database_cursor is not None and self.database_table is not None:
            cmd = "SELECT id FROM {0} ORDER BY id DESC LIMIT 1".format(self.database_table)
            self.database_cursor.execute(cmd)
            return self.database_cursor.fetchone()

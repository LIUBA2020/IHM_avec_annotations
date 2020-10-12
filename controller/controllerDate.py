from modele.imageDisplay import ImageDisplay
import os
import time

BASE_DIRECTORY = 'Aprex'

MONTH_NAME = ['Jan',
              'Feb',
              'Mar',
              'Apr',
              'May',
              'Jun',
              'Jul',
              'Aug',
              'Sep',
              'Oct',
              'Nov',
              'Dec']

IMAGE_EXTENSION = ['.jpg', '.png']


class ControllerDate:

    def __init__(self, model: ImageDisplay):
        self.model = model
        self.automatic_thread_running = True

    def set_date(self, day: int, month: int, year: int):
        """
        Register date.
        :param day: int, between 1 and 7
        :param month: int, between 1 and 12
        :param year: int
        """

        self.model.day = day
        self.model.month = month
        self.model.month_short_name = MONTH_NAME[month - 1]
        self.model.year = year

    def set_id(self, id: int):
        """
        Register id
        :param id: int
        """

        self.model.id = id

    def connect_to_most_recent_database(self, update_callback):
        """
        Thread to search for the most recent database, either the one corresponding to the current day or
        the most recent one. Called when the automatic mode is launched.
        :param update_callback: signal to update the UI.
        """

        while self.automatic_thread_running:
            time.sleep(0.2)

            # First, search database of the current day.
            self.__save_system_time_as_next_path()
            self.model.database_path = os.path.join(BASE_DIRECTORY,
                            str(self.model.year) + '_' + self.model.month_short_name + '_' + str(self.model.day).zfill(2),
                            'database.db')

            # If there is not, search for the most recent database.
            if not os.path.exists(self.model.database_path):
                self.__find_most_recent_dir()

            # Try to connect.
            ret = self.model.connect_to_database()
            if ret:
                # If connection is ok, search for last entry in database. Register new directory corresponding.
                self.model.choose_table()
                id = self.model.retrieve_last_entry()[0]
                self.model.dir = os.path.join(BASE_DIRECTORY,
                            str(self.model.year) + '_' + self.model.month_short_name + '_' + str(self.model.day).zfill(2),
                            str(id))
                self.model.id = id
                self.disconnect()

            # Update emit : ask UI to set a new date and id, hence showing new images if some are found.
            update_callback.emit()

    def connect_to_database(self):
        """
        Try to connect to database in directory with current year / name / day.
        :return: True if connection is ok, false if not.
        """

        path = os.path.join(BASE_DIRECTORY,
                            str(self.model.year) + '_' + self.model.month_short_name + '_' + str(self.model.day).zfill(2),
                            'database.db')

        self.model.database_path = path
        ret = self.model.connect_to_database()
        if ret:
            self.model.choose_table()

        return ret

    def disconnect(self):
        """
        Disconnect from database if a connection is already established.
        """

        self.model.disconnect_from_database()

    def retrieve_conformity(self):
        """
        Retrieve conformity from database. Emit the signal to display the new status.
        """

        conformity = self.model.retrieve_conformity_from_id(self.model.id)
        if conformity == 0:
            conformity = 'Status : improper'
        elif conformity == 1:
            conformity = 'Status : compliant'
        else:
            conformity = 'Can\'t find a conformity status'

        self.model.display_status_msg.emit(conformity)

    def check_directory_and_image(self):
        """
        Check if directory created from register year / month / day / id exists and if there is two images to retrieve.
        :return: True if directory and images exists, False on the contrary.
        """

        if self.model.day is None or self.model.id is None:
            return False

        check_dir = str(self.model.year) + '_' + self.model.month_short_name + '_' + str(self.model.day).zfill(2)
        check_dir = os.path.join(BASE_DIRECTORY, check_dir, str(self.model.id))

        if os.path.exists(check_dir):
            if self.__check_img(check_dir):
                self.model.dir = check_dir
                return True
            else:
                return False
        else:
            return False

    def __check_img(self, this_dir: str):
        """
        Check if there is two images in the directory
        :param this_dir: str, path to directory in which we need to search the images
        :return: True if images are found, False if not.
        """

        files = os.listdir(this_dir)
        check = [any(file.endswith(ext) for ext in IMAGE_EXTENSION) for file in files]
        if check.count(True) == len(check):
            self.model.img = files
            return True
        else:
            return False

    def __save_system_time_as_next_path(self):
        """
        Get current date and save it into model.
        """

        t = time.localtime()
        current_time = time.strftime("%D", t)

        self.model.month = int(current_time[0:2]) - 1
        self.model.month_short_name = MONTH_NAME[self.model.month]
        self.model.day = int(current_time[3:5])
        self.model.year = 2000 + int(current_time[6:])

    def __find_most_recent_dir(self):
        """
        Find most recently modified directory in which there is a "database.db" file.
        """

        all_subdirs = [os.path.join(BASE_DIRECTORY, d) for d in os.listdir(BASE_DIRECTORY)
                       if os.path.isdir(os.path.join(BASE_DIRECTORY, d))]
        latest_subdir = max(all_subdirs, key=os.path.getmtime)
        latest_subdir_basename = os.path.basename(latest_subdir)

        if len(latest_subdir_basename.split('_')) == 3:
            self.model.year = int(latest_subdir_basename.split('_')[0])
            self.model.month_short_name = latest_subdir_basename.split('_')[1]
            self.model.month = MONTH_NAME.index(self.model.month_short_name)
            self.model.day = int(latest_subdir_basename.split('_')[2])

            self.model.database_path = os.path.join(BASE_DIRECTORY,
                            str(self.model.year) + '_' + self.model.month_short_name + '_' + str(self.model.day).zfill(2),
                            'database.db')

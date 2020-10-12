from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets

from GUI.mainWindow import Ui_MainWindow
from controller.controllerImage import ControllerImage


class ViewImage:

    def __init__(self, ui: Ui_MainWindow, controller: ControllerImage):
        # Set up UI
        self.ui = ui
        self.controller = controller

        # Prepare to register two images.
        self.pixmap1 = None
        self.pixmap2 = None

        # Connect signals to function
        self.controller.model.image_found.connect(self.__display_image)
        self.controller.model.clear_image.connect(self.__clear_image)
        self.controller.model.display_status_msg.connect(self.__update_status)

    def __del__(self):
        pass

    def resize(self):
        """
        Called by resize_event in ViewMain. Resize image if window is resized.
        """

        if self.pixmap1 is not None and self.pixmap2 is not None:
            pixmap1 = self.pixmap1.scaled(self.ui.label_img1.size(), QtCore.Qt.KeepAspectRatio)
            pixmap2 = self.pixmap2.scaled(self.ui.label_img2.size(), QtCore.Qt.KeepAspectRatio)
            self.ui.label_img1.setPixmap(pixmap1)
            self.ui.label_img2.setPixmap(pixmap2)

    def __display_image(self):
        """
        Get found image path and display them.
        """

        image_path = self.controller.get_image_path()
        self.pixmap1 = QPixmap(image_path[0])
        self.pixmap2 = QPixmap(image_path[1])

        self.ui.label_img1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ui.label_img2.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.resize()

    def __clear_image(self):
        """
        Clear image.
        """

        self.ui.label_img1.clear()
        self.ui.label_img1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ui.label_img2.clear()
        self.ui.label_img2.setFrameShape(QtWidgets.QFrame.StyledPanel)

    def __update_status(self, msg: str):
        """
        Set text in the status label.
        :param msg: message to display
        """

        self.ui.label_status_active.setText(msg)

from PyQt5 import QtWidgets, QtCore, QtGui
from GUI.mainWindow import Ui_MainWindow

from modele.imageDisplay import ImageDisplay

from controller.controllerImage import ControllerImage
from controller.controllerDate import ControllerDate

from view.viewImage import ViewImage
from view.viewDate import ViewDate


class ViewMain(QtWidgets.QMainWindow):

    def __init__(self):
        super(ViewMain, self).__init__()

        # Set ui and title
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Simple Image Display')

        # Create model, associate controller to corresponding view
        self.model = ImageDisplay()
        self.views = [ViewImage(self.ui, ControllerImage(self.model)),
                      ViewDate(self.ui, ControllerDate(self.model))]

    def stop_thread(self):
        """
        Ensure that the thread has been stopped if it is running when closing the software.
        """

        import time
        self.views[1].controller.automatic_thread_running = False
        time.sleep(1)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        Each time the window is resized, ask ViewImage to resize the pixmap.
        """

        self.views[0].resize()

        super(ViewMain, self).resizeEvent(event)

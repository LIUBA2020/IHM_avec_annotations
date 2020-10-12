import sys

from PyQt5 import QtWidgets
from view.viewMain import ViewMain


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_view = ViewMain()
    main_view.showMaximized()
    app.aboutToQuit.connect(main_view.stop_thread)
    app.exec()

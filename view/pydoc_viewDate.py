import pydoc
from view import viewDate
from GUI.mainWindow import Ui_MainWindow
from controller.controllerDate import ControllerDate
from view.viewDate import ViewDate

h =pydoc.render_doc(ViewDate)
print (h)
import pydoc
from view import viewImage
from GUI.mainWindow import Ui_MainWindow
from controller.controllerDate import ControllerDate
from view.viewImage import ViewImage

h =pydoc.render_doc(ViewImage)
print (h)
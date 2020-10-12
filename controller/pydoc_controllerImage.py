import pydoc
from controller.controllerImage import ControllerImage

h = pydoc.render_doc(ControllerImage)
print (h)
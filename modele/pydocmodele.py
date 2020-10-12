import pydoc
from controller.controllerImage import ControllerImage
from modele.imageDisplay import ImageDisplay
h = pydoc.render_doc(ImageDisplay)
print (h)
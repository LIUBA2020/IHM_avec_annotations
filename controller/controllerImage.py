import os
from modele.imageDisplay import ImageDisplay


class ControllerImage:

    def __init__(self, model: ImageDisplay):
        self.model = model

    def get_image_path(self):
        """
        Retrieve image path from informations registered in the model.
        :return: List containing the images path.
        """

        image_list = [os.path.join(self.model.dir, img_path) for img_path in self.model.img]
        return image_list

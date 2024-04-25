import numpy as np
from PIL import Image
import os

class ImportImage:
    image_folder = os.path.join(os.path.dirname(os.getcwd()), "resources")
    
    def __init__(self, file_name = "true_color01.png"):
        self.file_name = file_name
        self.file_path = os.path.join(self.image_folder, file_name)
        self.color_image = None

        self.load_image()

    def load_image(self):
        color_image = Image.open(self.file_path)

        # Convert the image to a numpy array 
        self.color_image = np.array(color_image)
        self.color_image = np.swapaxes(self.color_image, 0, 1)
        self.crop_image()

    def crop_image(self):
        # Crop the color image to remove the white border
        # Find the first and last rows and columns that are not white
        map_selection = np.where(self.color_image != 255)

        first_row = map_selection[0][0] + 1
        last_row = map_selection[0][-1] - 1
        first_col = map_selection[1][0] + 1
        last_col = map_selection[1][-1] - 1

        # Crop the image
        cropped_image = self.color_image[first_row : last_row, first_col : last_col]

        self.color_image = cropped_image


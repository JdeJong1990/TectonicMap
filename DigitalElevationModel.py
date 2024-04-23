#%%
import numpy as np
from PIL import Image
import os

class DigitalElevationModel:
    masks_folder = os.path.join(os.path.dirname(os.getcwd()), "resources")
    
    def __init__(self, file_name = "DEM_earth.png"):
        self.file_name = file_name
        self.file_path = os.path.join(self.masks_folder, file_name)
        self.color_image = None

        self.load_masks()

    def load_masks(self):
        color_image = Image.open(self.file_path)

        # Convert the image to a numpy array and isolate the red channel
        color_image_np = np.array(color_image)
        self.color_image = color_image_np[:, :, 0]
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
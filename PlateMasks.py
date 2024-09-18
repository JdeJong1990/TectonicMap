#%%
import numpy as np
from PIL import Image
import os

class PlateMasks:
    """ 
    This class loads the masks of the tectonic plates from an image file.
    The masks are used to determine which pixels belong to which tectonic plate.
    The image is a world map where each tectonic plate is represented by a unique grayscale value.
    """
    masks_folder = os.path.join(os.path.dirname(os.getcwd()), "resources")
    
    def __init__(self, masks_name = "test03_NoLines.png"):
        self.masks_name = masks_name
        self.masks_path = os.path.join(self.masks_folder, masks_name)
        self.masks = None
        self.color_image = None
        self.number_of_plates = 0

        self.load_masks()

    def load_masks(self):
        color_image = Image.open(self.masks_path)

        # Convert the image to a numpy array and isolate the red channel (of the grayscale image)
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
        cropped_image = self.color_image[first_row:last_row, first_col:last_col]
        self.color_image = cropped_image

        self.index_plates()

    def index_plates(self):
        """ 
        This method indexes the tectonic plates in the image.
        """
        # Get the unique values and their counts
        unique_values, counts = np.unique(self.color_image, return_counts=True)

        # Determine one percent of the total number of pixels
        threshold = 1000

        # Filter values that occur more than 100 times
        significant_values = unique_values[counts > threshold]

        # Map significant values to their new indices, and use 255 for others
        masks_by_index = np.full(self.color_image.shape, 255)  # Default all to 255

        for index, value in enumerate(significant_values):
            # Wherever plate_image equals the significant value, set it to the new index
            masks_by_index[self.color_image == value] = index

        self.masks = np.swapaxes(masks_by_index, 0, 1) # Transpose the image so that the first index is the longitude
        self.number_of_plates = len(significant_values)-1



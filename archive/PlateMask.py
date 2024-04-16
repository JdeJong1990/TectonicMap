#%%
import numpy as np
from PIL import Image
import os

class PlateMasks:
    masks_folder = "E:/Hobbie/tectonic_poster/tectonic_plates_project"
    
    def __init__(self, masks_name = "test03_NoLines.png"):
        self.masks_name = masks_name
        self.masks_path = os.path.join(self.masks_folder, masks_name)
        self.masks = None
        self.color_image = None
        self.number_of_plates = 0

        self.load_masks()

    def load_masks(self):
        color_image = Image.open(self.masks_path)

        # Convert the image to a numpy array and select the red channel
        color_image_np = np.array(color_image)
        self.color_image = color_image_np[:, :, 0]
        self.crop_image()

    def crop_image(self):
        # crop the color image to remove the white border
        # Find the first and last rows and columns that are not white
        first_row = np.where(self.color_image != 255)[0][0]
        last_row = np.where(self.color_image != 255)[0][-1]
        first_col = np.where(self.color_image != 255)[1][0]
        last_col = np.where(self.color_image != 255)[1][-1]

        # Crop the image
        cropped_image = self.color_image[first_row:last_row, first_col:last_col]
        self.color_image = cropped_image

        self.index_plates()

    def index_plates(self):
        # Get the unique values and their counts
        unique_values, counts = np.unique(self.color_image, return_counts=True)

        # Determine one percent of the total number of pixels
        threshold = 1000 #int(masks_image.shape[0] * masks_image.shape[1])

        # Filter values that occur more than 100 times
        significant_values = unique_values[counts > threshold]

        # Map significant values to their new indices, and use 255 for others
        masks_by_index = np.full(self.color_image.shape, 255)  # Default all to 255

        for index, value in enumerate(significant_values):
            # Wherever plate_image equals the significant value, set it to the new index
            masks_by_index[self.color_image == value] = index

        self.masks = np.swapaxes(masks_by_index, 0, 1)
        self.number_of_plates = len(significant_values)-1

#%%
import matplotlib.pyplot as plt
my_masks = PlateMasks()

plt.figure(1)
plt.imshow(my_masks.masks, cmap='gray')
plt.show()
print('first image shown')

from Plate import Plate

plate_index = 20

print('start making plate and find center')
my_plate = Plate(my_masks.masks==plate_index)


center = my_plate.center_coordinate
print("center determiend by Plate class: ", center)
[longigude, latitude] = center

def coordinate_to_pixel(longigude, latitude):
    x = (longigude+np.pi)/2/np.pi*4454+4454/2
    y = (latitude+np.pi/2)/np.pi*2227
    x = x%4454
    return x, y

#%%
plt.figure(2)
map = np.transpose(my_masks.masks==plate_index)
plt.imshow(map, cmap='gray', origin='lower')

x, y = coordinate_to_pixel(longigude, latitude)
plt.scatter(y, x, color='r', s=10)
plt.scatter(2000,4000, color='b', s=50)
plt.scatter(0,0, color='b', s=50)

plt.show()


print("second image shown")
# %%

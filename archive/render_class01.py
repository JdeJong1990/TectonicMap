import numpy as np
from PIL import Image
import os

from PlateMask import PlateMasks

class Poster:
    def __init__(self, resolution):
        self.resolution = resolution
        self.globes = []
        self.poster_pixels = np.zeros((resolution[1], resolution[0], 3), dtype=np.float32)
        self.plate_indices = None
        self.masks = PlateMasks()

    def render(self):
        # Go through every pixel in the poster, and determine the color of the pixel
        for x in range(self.resolution[0]):
            for y in range(self.resolution[1]):
                pixel_color = self.calculate_pixel_color([x, y])
                self.poster_pixels[y, x] = pixel_color
        self.save_image()

    def calculate_pixel_color(self, pixel_position):
        for globe in self.globes:
            if globe.check_on_plate(pixel_position):
                return np.array([0.0, 0.0, 0.0], dtype=np.float32)
            else:
                return np.array([1.0, 1.0, 1.0], dtype=np.float32)
            
    def save_image(self):
        # Normalize the pixel values to 0-255 range for image saving
        normalized_pixels = (self.poster_pixels * 255).astype(np.uint8)
        image = Image.fromarray(normalized_pixels, 'RGB')
        image.save('poster_image.png')

class Globe: 
    relative_radius = 0.1
    
    def __init__(self, plate_index, center_on_poster = [0, 0]):
        self.plate_index = plate_index
        self.center_on_poster = center_on_poster
        self.relative_radius = relative_radius
        self.orientation = [0 , 0]
        self.plate_mask = None

    def calculate_cordinate_at_position(self, position):
        return [0 , 0]
    
    def check_on_plate(self, coordinate):
        return True	
        
class plate_mask:
    def __init__(self, gray_value):
        self.gray_value = gray_value
        self.position_offset = [0 , 0]
        self.center_position = self.calculate_plate_center()

    def calculate_plate_center(self):

        return [0 , 0]

    def load_plates_mask(self):
        image = Image.open(self.plates_mask_path)
        return image

    def check_on_plate(self, coordinate):
        return True
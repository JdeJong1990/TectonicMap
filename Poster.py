
from datetime import datetime
import os

import numpy as np
from PIL import Image

from Coordinates import Coordinates
from Coordinates import PixelPosition
from Coordinates import RelativePosition
from Plate import Plate
from Globe import Globe
from PlateMasks import PlateMasks

class Poster:
    def __init__(self, resolution):
        """Initialize the poster with a specific resolution."""
        self.resolution = resolution
        self.globes = []
        self.poster_pixels = np.ones((resolution[0], resolution[1], 3), dtype=np.uint8)*255
        self.poster_pixels[:,:,0] = 135
        self.poster_pixels[:,:,1] = 206
        self.poster_pixels[:,:,2] = 235
        self.masks = PlateMasks()
        self.relative_radius = 0.25
        self.lighting_vector = np.array([1.0, -1.0, 1.0])*np.sqrt(3)/3
        self.height_map = np.zeros((resolution[0], resolution[1]), dtype=np.float32)

        print('Creating globes')
        for plate_index in range(0, self.masks.number_of_plates):
            self.globes.append(Globe(self.masks.masks == plate_index, radius_in_pixels = self.resolution[1]*self.relative_radius))
            
            # Print the progress
            print(f'\r[{"#" * (      plate_index // (46 // 20))}{" " * (20 - (plate_index // (46 // 20)))}] {plate_index/(47 - 1)*100+1.0:.1f}%', end='') 

    def render(self):
        # Go through every pixel in the poster, and determine the color of the pixel
        print('\nRendering image')
        for x in range(self.resolution[0]):
            for y in range(self.resolution[1]):
                poster_pixel_position = PixelPosition(x, y)
                self.calculate_pixel_layers(poster_pixel_position)

            # Print the progress
            print(f'\r[{"#" * (x // (self.resolution[0] // 20))}{" " * (20 - (x // (self.resolution[0] // 20)))}] {x/self.resolution[0]*100+0.5:.1f}%', end='')

        print('\n')        

    def calculate_pixel_layers(self, poster_pixel_position):
        for globe in self.globes:
            position_on_globe_mask = poster_pixel_position - globe.relative_center_on_poster*self.resolution[1] - PixelPosition(-globe.radius_in_pixels, -globe.radius_in_pixels)
            if globe.is_on_plate(position_on_globe_mask):
                layer_pixels = globe.calculate_pixel(position_on_globe_mask)
                self.fill_layers_with_pixels(layer_pixels, poster_pixel_position)
    
    def fill_layers_with_pixels(self, layer_pixels, poster_pixel_position):
        lighting_factor = np.clip(layer_pixels.normal_vector @ self.lighting_vector, 0, 1)
        color = layer_pixels.color*lighting_factor*255
        self.poster_pixels[poster_pixel_position.x,poster_pixel_position.y] = color
        self.height_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.height

    def save_image(self):
        """
        Saves the RGB image, ensuring all pixel values are clipped within the valid range
        for an 8-bit image (0 to 255). 
        """ 
        # Ensure all pixel values are within the 0 to 255 range
        clipped_pixels = np.clip(self.poster_pixels, 0, 255)
        clipped_pixels = clipped_pixels.astype(np.uint8)

        # Create an RGB image from the clipped pixel data
        image = Image.fromarray(clipped_pixels, 'RGB')

        image = image.transpose(Image.TRANSPOSE)
        
        save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, 'images')
    
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        full_save_path = os.path.join(save_path, f'poster_image_{timestamp}.png')
        
        # Save the image
        image.save(full_save_path)

        print('Image saved')

    def cmap(nindex):
        return [nindex,
                4*(nindex-0.5)**2,
                (1-nindex)]

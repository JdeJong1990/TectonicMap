
from datetime import datetime
import os

import numpy as np
from PIL import Image

from Coordinates import Coordinates
from Coordinates import PixelPosition
from Coordinates import RelativePosition

from Globe import Globe
from PlateMasks import PlateMasks
from scipy.ndimage import gaussian_filter

class Poster:
    def __init__(self, resolution):
        """Initialize the poster with a specific resolution."""
        self.resolution = resolution
        self.relative_radius = 0.25
        self.globes = []

        self.lighting_vector = np.array([1.0, -1.0, 1.0])*np.sqrt(3)/3

        self.color_map = np.zeros((resolution[0], resolution[1], 3), dtype=np.uint8)*255
        # self.color_map[:,:,0] = 135
        # self.color_map[:,:,1] = 206
        # self.color_map[:,:,2] = 235
        
        self.masks = PlateMasks()

        self.normal_map = np.zeros((resolution[0], resolution[1], 3))
        self.normal_map[:,:,0] = 1

        self.height_map = np.zeros((resolution[0], resolution[1]), dtype=np.float32)
        
        self.direct_lighting = np.zeros((resolution[0], resolution[1]), dtype=np.float32)
        self.ambient_occlusion = np.zeros((resolution[0], resolution[1]), dtype=np.float32)

        self.poster_pixels = np.zeros((resolution[0], resolution[1], 3), dtype=np.float32)

        print('Creating globes')
        for plate_index in range(0, self.masks.number_of_plates):
            self.globes.append(Globe(self.masks.masks == plate_index, radius_in_pixels = self.resolution[1]*self.relative_radius))
            
            # Print the progress
            print(f'\r[{"#" * (plate_index * 25 // (self.masks.number_of_plates - 1))}{" " * (25 - (plate_index * 25 // (self.masks.number_of_plates - 1)))}] {plate_index/(self.masks.number_of_plates - 1)*100:.1f}%', end='')

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

        self.calculate_ambient_occlusion()     
        self.combine_layers()

    def calculate_pixel_layers(self, poster_pixel_position):
        for globe in self.globes:
            position_on_globe_mask = (poster_pixel_position - globe.relative_center_on_poster*self.resolution[1] 
                                       - PixelPosition(-globe.radius_in_pixels, -globe.radius_in_pixels))
            if globe.is_on_plate(position_on_globe_mask):
                layer_pixels = globe.calculate_pixel(position_on_globe_mask)        # pixel object
                self.fill_layers_with_pixels(layer_pixels, poster_pixel_position)
    
    def fill_layers_with_pixels(self, layer_pixels, poster_pixel_position):
        lighting_factor = np.clip(layer_pixels.normal_vector @ self.lighting_vector, 0, 1)
        self.direct_lighting = lighting_factor
        
        self.normal_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.normal_vector
        self.height_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.height
        self.color_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.color

    def calculate_ambient_occlusion(self):
        print('Calculating ambient occlusion')
        blurred_height_map = gaussian_filter(self.height_map, sigma=self.resolution[1]/20)
        self.ambient_occlusion = self.height_map - blurred_height_map + 1
        print('Ambient occlusion calculated')

    def combine_layers(self):
        self.poster_pixels = self.color_map * (self.ambient_occlusion[:, :, np.newaxis]
                                             * self.direct_lighting)

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
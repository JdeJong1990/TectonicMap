
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
    """
    This class is used to create a poster with a specific resolution.
    The poster is created by combining multiple globes, each representing a tectonic plate.
    """
    def __init__(self, resolution):
        #Initialize the poster with a specific resolution.
        self.resolution = resolution
        self.relative_radius = 0.25
        self.globes = []

        self.lighting_vector = np.array([1.0, -1.0, 1.0])*np.sqrt(3)/3

        self.color_map = np.zeros((resolution[0], resolution[1], 3), dtype=np.uint8)*255
        
        self.masks = PlateMasks()

        # Create different layers for the poster, that are combined to create the final image
        self.normal_map = np.zeros((resolution[0], resolution[1], 3))
        self.normal_map[:,:,0] = 1

        self.height_map = np.zeros((resolution[0], resolution[1]), dtype=np.float32)
        self.altitude_map = np.zeros((resolution[0], resolution[1]), dtype=np.float32)
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
        # Fill the different layers of the poster with data, based on pixel objects from the globes
        for globe in self.globes:
            position_on_globe_mask = (poster_pixel_position - globe.relative_center_on_poster*self.resolution[1] 
                                       - PixelPosition(-globe.radius_in_pixels, -globe.radius_in_pixels))
            if globe.is_on_plate(position_on_globe_mask):
                layer_pixels = globe.calculate_pixel(position_on_globe_mask)        # pixel object
                self.fill_layers_with_pixels(layer_pixels, poster_pixel_position)
    
    def fill_layers_with_pixels(self, layer_pixels, poster_pixel_position):
        # Store the pixel data in the different layers of the poster
        lighting_factor = np.clip(layer_pixels.normal_vector @ self.lighting_vector, 0, 1)
        self.direct_lighting = lighting_factor
        
        self.normal_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.normal_vector
        self.height_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.height
        self.color_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.color
        self.altitude_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.altitude
        
    def calculate_ambient_occlusion(self):
        # Approximate ambient occlusion with a spacial high pass filter on the altitude map
        altitude_map = self.altitude_map
        blurred_altitude_map = gaussian_filter(altitude_map, sigma=self.resolution[1]/100)
        ambient_occlusion = altitude_map - blurred_altitude_map
        ambient_occlusion = (ambient_occlusion - np.min(ambient_occlusion)) / (np.max(ambient_occlusion) - np.min(ambient_occlusion))
        self.ambient_occlusion = ambient_occlusion

    def combine_layers(self):
        self.poster_pixels = self.color_map * (self.ambient_occlusion[:, :, np.newaxis]
                                             * self.direct_lighting)
        
    def save_image(self, image_matrix = None):
        """
        Saves the RGB image, ensuring all pixel values are clipped within the valid range
        for an 8-bit image (0 to 255). 
        """ 
        if image_matrix is None:
            image_matrix = self.poster_pixels
        else:
            # Normalize the image matrix to the range 0 to 255
            normalized = (image_matrix - np.min(image_matrix)) / (np.max(image_matrix) - np.min(image_matrix))
            image_matrix = normalized * 255
            image_matrix = np.repeat(image_matrix[:, :, np.newaxis], 3, axis=2)
    
        # Ensure all pixel values are within the 0 to 255 range
        clipped_pixels = np.clip(image_matrix, 0, 255)
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
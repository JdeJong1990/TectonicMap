
from datetime import datetime

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
        self.poster_pixels = np.zeros((resolution[0], resolution[1], 3), dtype=np.uint8)
        self.masks = PlateMasks()
        self.relative_radius = 0.25

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
        self.save_image()
        print('Image saved')

    def calculate_pixel_layers(self, poster_pixel_position):
        for globe in self.globes:
            position_on_globe_mask = poster_pixel_position - globe.relative_center_on_poster*self.resolution[1]
            if globe.is_on_plate(position_on_globe_mask):
                layer_pixels = globe.calculate_pixel(position_on_globe_mask)
                self.fill_layers_with_pixels(layer_pixels, poster_pixel_position)
    
    def fill_layers_with_pixels(self, layer_pixels, poster_pixel_position):
        self.poster_pixels[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.color
            
    def save_image(self):
        # Normalize the pixel values to 0-255 range for image saving
        normalized_pixels = (self.poster_pixels * 255).astype(np.uint8)

        image = Image.fromarray(normalized_pixels, 'RGB')

        # Rotate the image 90 degrees clockwise
        image = image.transpose(Image.ROTATE_270)

        # Add a timestamp to the filename for unique filenames
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        image.save(f'poster_image_{timestamp}.png')

    def cmap(nindex):
        return [nindex,
                4*(nindex-0.5)**2,
                (1-nindex)]

from datetime import datetime
import numpy as np
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
    def __init__(self, line_height, plates = None, relative_selection = [[0,1],[0,1]]):
        #Initialize the poster with a specific resolution.
        self.line_hight = line_height  # 1/(number of pixels vertically)
        resolution = np.array([int(2/line_height), int(1/line_height)]) 
        print(f'resolution: {resolution[0]}, {resolution[1]}')
        self.resolution = resolution

        # size of the poster in pixels
        size = np.array([2 * (relative_selection[0][1] - relative_selection[0][0]), relative_selection[1][1] - relative_selection[1][0]])/line_height
        size = [int(size[0]) , int(size[1])]   
        self.size = size
        print(f'size of poster: {size[0]}, {size[1]}')

        self.relative_selection = np.array(relative_selection)
        self.relative_radius = 0.225
        self.globes = []

        self.lighting_vector = np.array([1.0, -1.0, 1.0])*np.sqrt(3)/3

        self.masks = PlateMasks()

        # Create different layers for the poster, that are combined to create the final image
        self.normal_map = np.zeros((size[0], size[1], 3))
        self.normal_map[:,:,0] = 1

        self.color_map = np.ones((size[0], size[1], 3), dtype=np.uint8)*255
        self.height_map = np.zeros((size[0], size[1]), dtype=np.float32)
        self.altitude_map = np.zeros((size[0], size[1]), dtype=np.float32)
        self.direct_lighting = np.ones((size[0], size[1]), dtype=np.float32)
        self.ambient_occlusion = np.ones((size[0], size[1]), dtype=np.float32)
        self.cast_shadow = np.ones((size[0], size[1]), dtype=np.float32)*10

        self.poster_pixels = np.ones((size[0], size[1], 3), dtype=np.float32)*255

        print('Creating globes')
        if (plates == None): plates = range(0, self.masks.number_of_plates)
        
        for plate_index in plates:
        # for plate_index in range(0, self.masks.number_of_plates):
            globe = Globe(self.masks.masks == plate_index, radius_in_pixels = self.relative_radius/ line_height)
            if plate_index == 43:
                globe.relative_center_on_poster.y += -0.11
                globe.relative_center_on_poster.x += 0.06

            self.globes.append(globe)
            
            # Print the progress
            print(f'\r[{"#" * (plate_index * 25 // (self.masks.number_of_plates - 1))}{" " * (25 - (plate_index * 25 // (self.masks.number_of_plates - 1)))}] {plate_index/(self.masks.number_of_plates - 1)*100:.1f}%', end='')

    def render(self):
        # Go through every pixel in the poster, and determine the color of the pixel
        print('\nRendering image')
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                poster_pixel_position = PixelPosition(x, y)
                self.calculate_pixel_layers(poster_pixel_position)

            # Print the progress
            print(f'\r[{"#" * (x // (self.size[0] // 20))}{" " * (20 - (x // (self.size[0] // 20)))}] {x/self.size[0]*100+0.5:.1f}%', end='')
 
        self.combine_layers()

    def calculate_pixel_layers(self, poster_pixel_position):
        # Fill the different layers of the poster with data, based on pixel objects from the globes
        for globe in self.globes:
            position_on_globe_mask = self.position_on_globe_mask(globe, poster_pixel_position)
            if globe.is_on_plate(position_on_globe_mask):
                layer_pixels = globe.calculate_pixel(position_on_globe_mask)        # pixel object
                self.fill_layers_with_pixels(layer_pixels, poster_pixel_position)
            
            # Regardless of whether we hit a plate or not, we need to calculate the dropped shadow on the background
            self.calculate_cast_shadow_distance(globe, poster_pixel_position)
    
    def position_on_globe_mask(self, globe, poster_pixel_position):
        """ Determine what pixel [x,y] this poster pixel position hits on the globe mask of a globe."""
        # Define the pixel coordinates of the top left of the poster on the map.
        line_height = self.line_hight
       
        poster_top_left_px = PixelPosition(2 * self.relative_selection[0][0]/line_height, self.relative_selection[1][0]/line_height)
        globe_center_map_px = PixelPosition(globe.relative_center_on_poster.x , globe.relative_center_on_poster.y) * (1/line_height)
        position_on_globe_mask = poster_pixel_position + poster_top_left_px - globe_center_map_px + PixelPosition(globe.radius_in_pixels, globe.radius_in_pixels)
        return position_on_globe_mask            

    def fill_layers_with_pixels(self, layer_pixels, poster_pixel_position):
        # Store the pixel data in the different layers of the poster
        lighting_factor = np.clip(layer_pixels.normal_vector @ self.lighting_vector, 0, 1)

        self.normal_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.normal_vector
        self.height_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.height
        self.color_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.color
        self.altitude_map[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.altitude
        self.ambient_occlusion[poster_pixel_position.x,poster_pixel_position.y] = layer_pixels.ambient_occlusion
    
    def calculate_cast_shadow_distance(self, globe, poster_pixel_position):
        """	
        Calculate the distance to the plate on the input Globe in the direction of the lighting vector.
        If it hits. Store the distance in the cast_shadow layer.
        """
        nearest_plate = self.cast_shadow[poster_pixel_position.x, poster_pixel_position.y]

        # Calculate the distance to the plate in the direction of the lighting vector
        current_distance = globe.cast_plate_distance(poster_pixel_position, self.lighting_vector, self.resolution)
        if current_distance:
            if current_distance < nearest_plate:
                self.cast_shadow[poster_pixel_position.x, poster_pixel_position.y] = current_distance

    def combine_layers(self):
        ambient_occlusion = np.repeat(self.ambient_occlusion[:, :, np.newaxis], 3, axis=2)
        height_map = np.repeat(self.height_map[:, :, np.newaxis], 3, axis=2)

        self.direct_lighting = np.clip(np.sum(self.normal_map * self.lighting_vector, axis=2), 0, 1)
        direct_lighting = np.repeat(self.direct_lighting[:, :, np.newaxis], 3, axis=2)

        cast_shadow = np.clip(self.cast_shadow, 1, 2) *255*0.5
        cast_shadow = gaussian_filter(cast_shadow, sigma=self.resolution[1]/100)

        poster_pixels = np.repeat(cast_shadow[:, :, np.newaxis], 3, axis=2)

        poster_pixels[height_map != 0] = self.color_map[height_map != 0] * direct_lighting[height_map != 0] * ambient_occlusion[height_map != 0]

        poster_pixels *= 1.5
        # poster_pixels = self.color_map * direct_lighting * ambient_occlusion
        poster_pixels = np.clip(poster_pixels, 0, 300)

        self.poster_pixels = poster_pixels
        
    def save_image(self, image_matrix = None, name = 'poster_image'):
        """
        Saves the RGB image, ensuring all pixel values are clipped within the valid range
        for an 8-bit image (0 to 255). 
        """ 
        print('Start image saving procedure.')
        if image_matrix is None:
            image_matrix = self.poster_pixels
            if image_matrix is None:
                print("No poster pixels in Poster object. Image saving aborted.")
                return
            
        # Normalize the image matrix to the range 0 to 255 if it's not the default poster_pixels
        if image_matrix is not self.poster_pixels:
            if np.min(image_matrix) != np.max(image_matrix):  # Avoid division by zero
                normalized = (image_matrix - np.min(image_matrix)) / (np.max(image_matrix) - np.min(image_matrix))
                image_matrix = normalized * 255
            else:
                image_matrix = np.zeros_like(image_matrix)  # If all values are the same, create a zero image
            # Expand grayscale (2D) to RGB (3D) if necessary
            if len(np.shape(image_matrix)) == 2:
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

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        full_save_path = os.path.join(save_path, f'{timestamp}_{name}.png')

        # Save the image
        image.save(full_save_path)

        print('Image saved')
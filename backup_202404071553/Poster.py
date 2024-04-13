from datetime import datetime

import numpy as np
from PIL import Image

from Plate import Plate
from PlateMasks import PlateMasks

class Poster:
    def __init__(self, resolution):
        self.resolution = resolution
        self.globes = []
        self.poster_pixels = np.ones((resolution[1], resolution[0], 3), dtype=np.float32)
        self.plate_indices = None
        self.masks = PlateMasks()

        for plate_index in range(1, self.masks.number_of_plates):
            self.globes.append(Globe(plate_index, self.masks.masks==plate_index))

    def render(self):
        # Go through every pixel in the poster, and determine the color of the pixel
        for x in range(self.resolution[0]):
            print(f'\r: [{"#" * (x // (self.resolution[0] // 20))}{" " * (20 - (x // (self.resolution[0] // 20)))}] {x/self.resolution[0]*100:.2f}%', end='')
            for y in range(self.resolution[1]):
                relative_pixel_position = np.array([x, y])/self.resolution[1]  
                self.poster_pixels[y, x] = self.calculate_pixel_color(relative_pixel_position)
        self.save_image()
        print('Image saved')

    def calculate_pixel_color(self, relative_pixel_position):
        for globe in self.globes:
            if globe.pixel_on_plate(relative_pixel_position):
                nindex = globe.plate_index/len(self.globes)
                return [nindex,
                        4*(nindex-0.5)**2,
                        1-nindex]
                        
    def save_image(self):
        # Normalize the pixel values to 0-255 range for image saving
        normalized_pixels = (self.poster_pixels * 255).astype(np.uint8)
        image = Image.fromarray(normalized_pixels, 'RGB')
        # Add a timestamp to the filename
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        image.save(f'poster_image_{timestamp}.png')

class Globe: 
    def __init__(self, plate_index, mask, relative_radius = 0.2):
        print(f"Creating globe with plate index {plate_index}")
        self.plate_index = plate_index
        self.relative_radius = relative_radius

        self.plate = Plate(mask)
        self.plate_coordinate = self.plate.center_coordinate
        self.relative_center_on_poster = np.array([0.5 , 0.5])

        self.calculate_position_on_poster()

    def calculate_position_on_poster(self):
        [longitude, latitude] = self.plate_coordinate
        self.relative_center_on_poster = [(longitude + np.pi)/2/np.pi*2, 
                                          -(latitude - np.pi/2)/np.pi]
    
    def pixel_on_plate(self, relative_pixel_position):
        if self.is_pixel_on_globe(relative_pixel_position):
            return self.is_pixel_on_plate(relative_pixel_position)

    def is_pixel_on_globe(self, relative_pixel_position):
        x_distance = abs(self.relative_center_on_poster[0] - relative_pixel_position[0])
        y_distance = abs(self.relative_center_on_poster[1] - relative_pixel_position[1])
        distance = np.sqrt(x_distance**2 + y_distance**2)
        return distance <= self.relative_radius
        
    def is_pixel_on_plate(self, relative_pixel_position):
        relative_globe_position = (relative_pixel_position - self.relative_center_on_poster)/self.relative_radius
        if self.globe_position_is_on_plate(relative_globe_position):
            return True
        
    def globe_position_is_on_plate(self, relative_globe_position):
        # A range of -1 to 1 is used to represent the globe for x and y
        # Convert the relative globe position to a 3D vector
        vector = np.array([np.sqrt(1 - relative_globe_position[0]**2 - relative_globe_position[1]**2),
                           relative_globe_position[0], 
                           relative_globe_position[1]])
        vector = vector / np.linalg.norm(vector)

        # Rotate the vector such that it corresponts to a position on a globe that turned (0,0) towards us
        vector_aligned = self.rotate_theta_phi(vector, self.plate_coordinate)

        # Convert the vector to a coordinate
        coordinate = self.vec3_to_coordinate(vector_aligned)

        # Convert the coordinate to a pixel
        [longitude, latitude] = coordinate
        [x, y] = self.coordinate_to_relative_pixel([longitude, latitude])

        # Check if the pixel is on the plate
        return self.plate.mask[int(x*self.plate.mask.shape[1]), 
                               int(y*self.plate.mask.shape[1])]
    
    def rotate_theta_phi(self, vector, plate_coordinate):
        longitude = plate_coordinate[0]
        latitude  = plate_coordinate[1]

        # Rotate the vector around the y-axis
        vector = np.array([[np.cos(latitude), 0, -np.sin(latitude)],
                           [0, 1, 0],
                           [np.sin(latitude), 0, np.cos(latitude)]]) @ vector
        
        # Rotate the vector around the z-axis
        vector = np.array([[np.cos(longitude), -np.sin(longitude), 0],
                           [np.sin(longitude), np.cos(longitude), 0],
                           [0, 0, 1]]) @ vector
        return vector
    
    def vec3_to_coordinate(self, vector):
        # Convert a 3D vector to a coordinate in longitude and latitude
        longitude_rad = np.arctan2(vector[1], vector[0])
        latitude_rad = np.arcsin(vector[2] / np.linalg.norm(vector))
        return np.array([longitude_rad, latitude_rad])
    
    def coordinate_to_relative_pixel(self, coordinate):
        # Convert a coordinate to a relative pixel on the poster
        longitude = coordinate[0]
        latitude = coordinate[1]
        x = 0.5 + longitude/2/np.pi
        y = 0.5 - latitude/np.pi
        return x, y
    
        

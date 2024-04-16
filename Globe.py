import numpy as np

from Coordinates import Coordinates
from Coordinates import RelativePosition
from Plate import Plate

class Globe: 
    def __init__(self, plate_index, masks, radius_in_pixels):
        print(f'\r[
              {"#" * (      plate_index // (46 // 20))}
              {" " * (20 - (plate_index // (46 // 20)))}] 
              {plate_index/(47 - 1)*100+1.0:.1f}%', end='') # Print the progress
    
        self.plate_index = plate_index
        self.radius_in_pixels = radius_in_pixels

        self.plate = Plate(masks == plate_index)        # this is a mask with a center coordinate
        self.plate_coordinate = self.plate.center_coordinate
        self.relative_center_on_poster = self.plate_coordinate.to_relative_position()

        self.radius_in_pixels = radius_in_pixels
        self.globe_mask = np.zeros((int(2 * radius_in_pixels), int(2 * radius_in_pixels), 3), dtype=np.float32)      # this is a mask the size of the globe

        self.make_globe_mask()

    def make_globe_mask(self):
        for x in range(int(2 * self.radius_in_pixels)):
            for y in range(int(2 * self.radius_in_pixels)):
                centered_globe_position = RelativePosition(x / (2 * self.radius_in_pixels)*2 - 1, y/(2 * self.radius_in_pixels)*2 - 1)
                self.globe_mask[x, y] = self.globe_position_is_on_plate(centered_globe_position)
    
    def globe_position_is_on_plate(self, centered_globe_position):
        # A range of -1 to 1 is used to represent the globe for x and y
        # Convert the relative globe position to a 3D vector

        squared_z_component  = 1 - centered_globe_position.x**2 - centered_globe_position.y**2

        if squared_z_component  < 0:
            return False
        
        vector = np.array([np.sqrt(squared_z_component ),
                           centered_globe_position.x, 
                           -centered_globe_position.y])
        
        # Rotate the vector such that it corresponts to a position on a globe that turned (0,0) towards us
        vector_aligned = self.rotate_theta_phi(vector, self.plate_coordinate)

        # Convert the vector to a coordinate
        coordinate = self.vec3_to_coordinate(vector_aligned)

        # Latitude used to be inverted (*-1)
        relative_position = coordinate.to_relative_position()
        
        # Check if the pixel is on the plate
        return self.plate.mask[int(relative_position.x*self.plate.mask.shape[1]), 
                               int(relative_position.y*self.plate.mask.shape[1])]
    
    def rotate_theta_phi(self, vector, plate_coordinate):
        longitude = plate_coordinate.longitude
        latitude  = plate_coordinate.latitude

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
        return Coordinates(longitude_rad, latitude_rad)
    
    def pixel_on_plate(self, relative_pixel_position):
        relative_position_on_globe = relative_pixel_position - self.relative_center_on_poster
        # Check if the pixel is on the plate
        return self.globe_mask[int(relative_pixel_position.x*self.radius_in_pixels), 
                               int(relative_pixel_position.y*self.radius_in_pixels)]
 
 #test
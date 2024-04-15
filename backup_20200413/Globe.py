import numpy as np

from Coordinates import Coordinates
from Plate import Plate

class Globe: 
    def __init__(self, plate_index, masks, relative_radius = 0.25):
        print(f'\r[{"#" * (plate_index // (46 // 20))}{" " * (20 - (plate_index // (46 // 20)))}] {plate_index/(np.max(masks) - 1)*100+1.0:.1f}%', end='')
            
        #print(f"Creating globe with plate index {plate_index}")
        self.plate_index = plate_index
        self.relative_radius = relative_radius

        self.plate = Plate(masks == plate_index)
        self.plate_coordinate = self.plate.center_coordinate
        self.relative_center_on_poster = None

        self.calculate_position_on_poster()

    def calculate_position_on_poster(self):
        plate_coordinate = self.plate_coordinate
        self.relative_center_on_poster = plate_coordinate.to_relative_position()
    
    def pixel_on_plate(self, relative_pixel_position):
        centered_globe_position = (relative_pixel_position - self.relative_center_on_poster)
        if self.is_pixel_on_globe(centered_globe_position):
            return self.globe_position_is_on_plate(centered_globe_position)

    def is_pixel_on_globe(self, centered_globe_position):
        distance_from_globe_center = centered_globe_position.to_magnitude()
        return distance_from_globe_center <= self.relative_radius

    def globe_position_is_on_plate(self, centered_globe_position):
        # A range of -1 to 1 is used to represent the globe for x and y
        # Convert the relative globe position to a 3D vector

        vector = np.array([np.sqrt(self.relative_radius**2 - centered_globe_position.x**2 - centered_globe_position.y**2),
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
 
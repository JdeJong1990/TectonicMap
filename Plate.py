#%%
import numpy as np

from Coordinates import Coordinates
class Plate:
    def __init__(self, mask):
        self.mask = mask
        self.center_coordinate = None

        self.find_center()

    def find_center(self):
        """
        Find the center of the tectonic plate
        Go through the mask, every pixel that is part of the plate is converted to a vector.
        The average of those vectors represents the center of the plate.
        Convert that back to a coordinate.
        """
        width = self.mask.shape[0]
        height = self.mask.shape[1]
        
        vectors = []

        for y in range(0, height, 10):
            for x in range(0, width, 10):
                if self.mask[x][y]:
                    longitute_rad = (x/height - 1.0) * np.pi
                    lattitude_rad = (0.5 - y/height) * np.pi
                    vector = np.array([np.cos(longitute_rad),
                                       np.sin(longitute_rad),
                                       np.sin(lattitude_rad)])
                    # correct for the effect that pixels close to the poles correspond to smaller areas. 
                    vectors.append(vector * np.cos(lattitude_rad))

        # Calculate the average of all vectors
        average_vector = np.mean(vectors, axis=0)

        self.center_coordinate = self.vec3_to_coordinate(average_vector) 

    def vec3_to_coordinate(self, vector):
        # Convert a vector to a coordinate on the poster
        longitude_rad = np.arctan2(vector[1], vector[0])
        latitude_rad = np.arcsin(vector[2] / np.linalg.norm(vector))
        return Coordinates(longitude_rad, latitude_rad)

#test
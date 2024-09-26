import numpy as np
from scipy.ndimage import gaussian_filter

from Coordinates import Coordinates
from Coordinates import PixelPosition
from Coordinates import RelativePosition
from ImportImage import ImportImage
from LayerPixels import LayerPixels
from Plate import Plate

class Globe: 
    """
    Class for creating a globe object. The globe object is a 3D representation of the earth.
    The globe object will show up on the map, where only one tectonic plate is visible.
    The tectonic plate is turned towards the viewer.
    """
    elevation_model = ImportImage(file_name = "DEM_earth.png")
    color_file = ImportImage(file_name = "true_color01.png")

    def __init__(self, mask, radius_in_pixels):
        self.radius_in_pixels = radius_in_pixels

        self.plate = Plate(mask)        # this is an object consisting of a mask in the shape of a tectonic plate  
        self.plate_coordinate = self.plate.center_coordinate 
        self.relative_center_on_poster = self.plate_coordinate.to_relative_position()

        # Create a number of layers for the chosen side of the globe
        self.globe_plate_mask = np.full((int(2 * self.radius_in_pixels), int(2 * self.radius_in_pixels)), False)
        self.normal_map = self.initialize_map_3(1, 0, 0)
        self.color_map         = np.full((int(2 * self.radius_in_pixels), int(2 * self.radius_in_pixels), 3), 0)
        self.height_map        = np.full((int(2 * self.radius_in_pixels), int(2 * self.radius_in_pixels)), 0.0, dtype=np.float32)
        self.ambient_occlusion = np.full((int(2 * self.radius_in_pixels), int(2 * self.radius_in_pixels)), 0.0, dtype=np.float32)
        self.altitude_map      = np.full((int(2 * self.radius_in_pixels), int(2 * self.radius_in_pixels)), 0.0, dtype=np.float32)
        self.altitude_factor = 0.0  # How big it the relief on the earth surface, relative to the radius of the earth
        
        # Fill the layers with data
        self.make_globe_layers()

    def initialize_map_3(self, first_value, second_value, third_value):
        map = np.zeros((int(2 * self.radius_in_pixels), int(2 * self.radius_in_pixels), 3), dtype=np.float32)      # this is a mask the size of the globe
        map[..., 0] = first_value
        map[..., 1] = second_value
        map[..., 2] = third_value
        return map

    def make_globe_layers(self):
        # Fill the layers with data
        for x in range(int(2 * self.radius_in_pixels)):
            for y in range(int(2 * self.radius_in_pixels)):
                centered_globe_position = RelativePosition( x/self.radius_in_pixels -1 , y/self.radius_in_pixels - 1)
                self.normal_map[x, y]       = self.calculate_normal_vector(centered_globe_position)
                self.globe_plate_mask[x, y] = self.globe_position_is_on_plate(centered_globe_position)
                self.altitude_map[x, y]     = self.calculate_altitude(centered_globe_position)
                self.color_map[x, y, :]     = self.calculate_color(centered_globe_position)
                self.height_map[x, y]       = self.calculate_height(PixelPosition(x,y))
        self.drop_height_map()
        self.calculate_ambient_occlusion()
    
    def calculate_normal_vector(self, centered_globe_position):
        # A range of -1 to 1 is used to represent the globe for x and y
        # Determine the z-component of the normal vector
        squared_z_component  = 1 - centered_globe_position.x**2 - centered_globe_position.y**2

        # Normalize the normal vector
        if squared_z_component  < 0:        # this is a check to see if the point is on the globe
            return np.array([1.0 , 0.0 , 0.0])
        else:
            normal_vector = np.array([np.sqrt(squared_z_component), 
                                        centered_globe_position.x, 
                                        -centered_globe_position.y])

            normal_vector = normal_vector / np.linalg.norm(normal_vector)
            return normal_vector

    def globe_position_is_on_plate(self, centered_globe_position):
        """ 
        This method checks if a pixel is on the  tectonic plate 
        Input is a relative position on the mask (x: -1 to 1, y: -1 to 1)
        Output is a boolean
        """
        relative_position = self.mask_position_on_globe(centered_globe_position)
        
        # Check if the pixel is on the plate
        return self.plate.mask[int(relative_position.x*self.plate.mask.shape[1]), 
                               int(relative_position.y*self.plate.mask.shape[1])]
    
    def calculate_altitude(self, centered_globe_position):
        # This method looks up the altitude of a pixel on the globe
        relative_position = self.mask_position_on_globe(centered_globe_position)
        normalized_altitude = float(Globe.elevation_model.color_image[int(relative_position.x*Globe.elevation_model.color_image.shape[1]), 
                                                                      int(relative_position.y*Globe.elevation_model.color_image.shape[1])][0]) / 255
        return normalized_altitude

    def calculate_ambient_occlusion(self):
        # This method calculates the ambient occlusion of a pixel on the globe
        altitude_map = self.altitude_map  
        
        blurred_altitude_map = gaussian_filter(altitude_map, sigma=np.max([self.radius_in_pixels/200,3]))
        high_pass_altitude = (altitude_map - blurred_altitude_map).astype(np.float32)
        
        ambient_occlusion = -np.log(abs(high_pass_altitude) + 1e-9)*np.clip(high_pass_altitude,-0.01,0.01)
        ambient_occlusion = ambient_occlusion*20 +1
        self.ambient_occlusion = ambient_occlusion/2
    
    def calculate_color(self, centered_globe_position):
        # This method looks up the color of a pixel on the globe
        relative_position = self.mask_position_on_globe(centered_globe_position)
        color = Globe.color_file.color_image[int(relative_position.x*Globe.color_file.color_image.shape[1]), 
                                            int(relative_position.y*Globe.color_file.color_image.shape[1]),
                                            :]
        return color

    def mask_position_on_globe(self, centered_globe_position):
        """
        This method converts a position on the mask of the globe (x: -1 to 1, y: -1 to 1)
        to a corresponding coordinate in (normalized) longitude and latitude on the globe.
        A range of -1 to 1 is used to represent the globe for x and y on the mask of the globe
        """
        # Convert the relative globe position to a 3D vector
        squared_z_component  = 1 - centered_globe_position.x**2 - centered_globe_position.y**2

        if squared_z_component  < 0:
            return RelativePosition(0, 0)
        
        vector = np.array([np.sqrt(squared_z_component ),
                           centered_globe_position.x, 
                           -centered_globe_position.y])
        
        # Rotate the vector such that it corresponts to a position on a globe that turned (0,0) towards us
        vector_aligned = self.rotate_theta_phi(vector, self.plate_coordinate)

        # Convert the vector to a coordinate
        coordinate = self.vec3_to_coordinate(vector_aligned)

        # Return the relative position
        return coordinate.to_relative_position()
        
    def rotate_theta_phi(self, vector, plate_coordinate):
        """
        Rotate the vector such that it corresponts to a position on a globe when we turn spherical coordinates,
        (1,theta,phi) towards the viewer
        """
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
        """ Convert a 3D vector to a coordinate in longitude and latitude"""
        longitude_rad = np.arctan2(vector[1], vector[0])
        latitude_rad = np.arcsin(vector[2] / np.linalg.norm(vector))
        return Coordinates(longitude_rad, latitude_rad)
    
    def is_on_plate(self, position_on_globe_mask):
        """ This method checks if a pixel is on the current tectonic plate """
        if self.position_is_on_globe_mask(position_on_globe_mask):
            return self.globe_plate_mask[int(position_on_globe_mask.x), int(position_on_globe_mask.y)]
        else:
            return False
    
    def position_is_on_globe_mask(self, position_on_globe_mask):
        """ This method checks if a pixel is on the globe mask."""
        x_diff = position_on_globe_mask.x - self.radius_in_pixels
        y_diff = position_on_globe_mask.y - self.radius_in_pixels
        squared_distance = x_diff**2 + y_diff**2
        threshold = 0.8 * self.radius_in_pixels**2
        return squared_distance < threshold
    
    def calculate_pixel(self, position_on_globe_mask):
        """ This method calculates the properties of a pixel on the globe"""
        pixel_object = LayerPixels()

        pixel_object.normal_vector            = self.normal_map[int(position_on_globe_mask.x), int(position_on_globe_mask.y)]
        pixel_object.color                    =  self.color_map[int(position_on_globe_mask.x), int(position_on_globe_mask.y)]   
        pixel_object.height                 = self.height_map[int(position_on_globe_mask.x), int(position_on_globe_mask.y)]
        pixel_object.altitude               = self.altitude_map[int(position_on_globe_mask.x), int(position_on_globe_mask.y)]
        pixel_object.ambient_occlusion = self.ambient_occlusion[int(position_on_globe_mask.x), int(position_on_globe_mask.y)]
        return pixel_object
    
    def calculate_height(self, position_on_globe_mask):
        """ This method looks up the height of a pixel on the globe"""
        if not self.is_on_plate(position_on_globe_mask):
            return 0

        position_altitude = self.altitude_map[int(position_on_globe_mask.x), int(position_on_globe_mask.y)]
        height_squared = (self.radius_in_pixels**2
                     - (position_on_globe_mask.x - self.radius_in_pixels)**2 
                     - (position_on_globe_mask.y - self.radius_in_pixels)**2)
        if height_squared > 0:
            shell_height = np.sqrt(height_squared) / self.radius_in_pixels
        else:
            shell_height = 0
    
        return shell_height
    
    def drop_height_map(self):
        # Take the height map and find the non-zero elements
        non_zero_elements = self.height_map[np.nonzero(self.height_map)]

        # Find the smallest element among the non-zero elements
        smallest_element = 0
        try:    # When the resolution is low, some plates don't show up on the poster, and there is no heigth
            smallest_element = np.min(non_zero_elements)
        except:
            pass

        # Lower all the non-zero elements by the smallest element
        self.height_map[np.nonzero(self.height_map)] -= smallest_element

    def cast_plate_distance(self, poster_pixel_position, lighting_vector, resolution):
        """ Calculate the distance to the plate in the direction of the lighting vector, if it hits """
        direction = -lighting_vector
        center = np.array([self.relative_center_on_poster.x, self.relative_center_on_poster.y, 0]) * resolution[1]
        position = np.array([poster_pixel_position.x, poster_pixel_position.y, 0])
        radius = self.radius_in_pixels

        # Check if we hit the globe
        b = -np.dot(direction, (center - position))
        c = np.dot(center - position, center - position) - radius**2

        discriminant = b**2 - c

        if discriminant < 0:
            return False

        # Calculate the distance to the plate in the direction of the lighting vector
        distance_1 = -b - np.sqrt(discriminant)
        distance_2 = -b + np.sqrt(discriminant)

        # Determine where on the mask we end up, following these distances
        position_1 = position + distance_1 * direction
        position_2 = position + distance_2 * direction

        # Check if we hit the plate
        relative_hit1 = (position_1 - center) / radius
        relative_hit2 = (position_2 - center) / radius

        if ((distance_1 > 0) and self.globe_position_is_on_plate(RelativePosition(relative_hit1[0], relative_hit1[1]))):
            return distance_1

        if ((distance_2 > 0) and self.globe_position_is_on_plate(RelativePosition(relative_hit2[0], relative_hit2[1]))):
            return distance_2

        return False
            


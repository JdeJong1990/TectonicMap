import numpy as np

class LayerPixels:
    # This class is used to store multiple properties of a pixel for the poster.
    def __init__(self):
        self.color = np.array([1.0 , 0.0 , 1.0])
        self.normal_vector = np.array([1.0 , 0.0 , 0.0])
        self.height = 0.0
        self.altitude = 0.0
        self.ambient_occlusion = 0.0
        
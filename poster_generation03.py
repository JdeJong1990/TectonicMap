"""
V3: We use line_height instead of resolution
"""

#%%
import numpy as np
import matplotlib
matplotlib.use('qt5agg')  # Or use 'tkagg' if 'qt5agg' doesn't work
import matplotlib.pyplot as plt

from Poster import Poster

#%%
plates = [33,40,2,21,27,6,15,20,30,31,41,43,47]
relative_selection = [[0.25,1],[0.5,1]]
relative_selection = [[0,1],[0,1]]

#%% antartic plate
plates =  [4, 7, 30, 37, 41, 43, 47]
relative_selection = [[0.5,0.8],[0.5,1]]
vertical_resolution = 200
line_height = 1/vertical_resolution
poster = Poster(line_height, plates = plates)
poster.render(relative_selection = relative_selection)
print('\nSaving image')
poster.save_image()

#%% Whole poster

vertical_resolution = 200
line_height = 1/vertical_resolution
plates = [2,6,15,20,21,27,30,31,33,40,41,43,47]
# relative_selection = [[0.5,1.0],[0.0,1.0]]
relative_selection = [[0.25,0.75],[0.4,0.6]]
# relative_selection = [[0.0,1],[0.0,1]]
poster = Poster(line_height, plates = plates)
# poster.render(relative_selection= relative_selection)
poster.render(relative_selection =relative_selection)
poster.save_image()
poster.save_image(poster.cast_shadow, 'cast_shadow')

#%% Test around North american plate
plates = [20]
relative_selection = [[0.2,0.35],[0.05,0.35]]
vertical_resolution = 12036
# vertical_resolution = 300
line_height = 1/vertical_resolution
poster = Poster(line_height, plates = plates, relative_selection = relative_selection)
poster.render()
poster.save_image()

#%% Save the different layers of the poster for debugging
poster.save_image(poster.ambient_occlusion, 'ambient_occlusion')
poster.save_image(poster.altitude_map, 'altitude_map')
poster.save_image(poster.color_map, 'color_map')
poster.save_image(poster.normal_map,'normal_map')
poster.save_image(poster.height_map, 'height_map')
poster.save_image(poster.cast_shadow, 'cast_shadow')

#%% Panel 1
relative_selection = [[-0.028,0.229],[0.202,0.703]]
plates =  [2, 15, 21, 27, 28 ,29, 32]

#%% Panel 2
relative_selection = [[0.161,0.366],[-0.011,0.392]]
plates =  [20]

# Panel 3
relative_selection = [[0.222,0.575],[0.277,0.78]]
plates =  [6, 10, 11, 12, 14, 19, 23, 28, 32, 34, 36, 46, 47]

#%% Panel 4
relative_selection = [[0.544,0.744],[0.052,0.651]]
plates =  [7, 30, 31, 37, 42, 44]
vertical_resolution = 12036
# vertical_resolution = 300
line_height = 1/vertical_resolution
poster = Poster(line_height, plates = plates, relative_selection = relative_selection)
poster.render()
poster.save_image()

#%% Panel 5
relative_selection = [[0.569,0.775],[0.557,0.96]]
plates =  [43]

# Panel 6
relative_selection = [[0.74,0.891],[0.117,0.52]]
plates = [
    0, 1, 3, 4, 5, 8, 13, 16, 17, 18, 
    24, 25, 26, 35, 38, 39, 45
]

# Panel 7
relative_selection = [[0.705,0.908],[0.45,0.755]]
plates = [41]

# Panel 8
relative_selection = [[0.903,0.953],[0.495,0.594]]
plates = [22, 33, 40]


# Ideas:
# Make light from cities in the shadow parts of the globes


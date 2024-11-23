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
vertical_resolution = 300
line_height = 1/vertical_resolution
poster = Poster(line_height, plates = plates, relative_selection = relative_selection)
poster.render()
print('\nSaving image')
poster.save_image()

#%% Whole poster

vertical_resolution = 50
line_height = 1/vertical_resolution
plates = [33,40,2,21,27,6,15,20,30,31,41,43,47]
poster = Poster(line_height, plates = plates)
poster.render()
poster.save_image()

#%% Test around North american plate
plates = [20]
relative_selection = [[0.2,0.35],[0.05,0.35]]
vertical_resolution = 12036
vertical_resolution = 300
line_height = 1/vertical_resolution
poster = Poster(line_height, plates = plates, relative_selection = relative_selection)
poster.render()
poster.save_image()

#%% Save the different layers of the poster for debugging
poster.save_image(poster.ambient_occlusion, 'ambient_occlusion')
poster.save_image(poster.altitude_map, 'altitude_map')
poster.save_image(poster.color_map, 'color_map')
# poster.save_image(poster.normal_map,'normal_map')
# poster.save_image(poster.height_map, 'height_map')
# poster.save_image(poster.cast_shadow, 'cast_shadow')

# Ideas:
# Make light from cities in the shadow parts of the globes


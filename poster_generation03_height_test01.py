"""
V3: We use line_height instead of resolution
"""

#%%
import numpy as np

import matplotlib
matplotlib.use('qt5agg')  # Or use 'tkagg' if 'qt5agg' doesn't work
import matplotlib.pyplot as plt

from Poster import Poster


#%% Whole poster

vertical_resolution = 600
line_height = 1/vertical_resolution
poster = Poster(line_height)
poster.render()
poster.save_image()
poster.save_image(poster.height_map, 'height_map')
poster.save_image(poster.cast_shadow, 'cast_shadow')

#%%
for i in range(poster.masks.number_of_plates):
    fig = plt.figure(1)
    ax = fig.add_subplot(1,1,1)
    ax.imshow(poster.globes[i].height_map)
    ax.set_title(f'Height map for plate {i}, minimum height: {np.min(poster.globes[i].height_map):.4f}')
    ax.axis('equal')
    ax.axis('off')
    plt.show()

# %%

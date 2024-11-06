#%%
import numpy as np
import matplotlib
matplotlib.use('qt5agg')  # Or use 'tkagg' if 'qt5agg' doesn't work
import matplotlib.pyplot as plt

from Poster import Poster

#%%

plates = [6,15,20,30,31,41,43,47]
relative_selection = [[0.25,1],[0.5,1]]
relative_selection = [[0,1],[0,1]]
poster = Poster([250, 100], plates = plates, relative_selection = relative_selection)
poster.render()
print('\nSaving image')
poster.save_image()

#%% Save the different layers of the poster for debugging
# poster.save_image(poster.ambient_occlusion, 'ambient_occlusion')
# poster.save_image(poster.altitude_map, 'altitude_map')
# poster.save_image(poster.color_map, 'color_map')
# poster.save_image(poster.normal_map,'normal_map')
# poster.save_image(poster.height_map, 'height_map')
# poster.save_image(poster.cast_shadow, 'cast_shadow')

# Ideas:
# Make light from cities in the shadow parts of the globes


# %%
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.imshow(poster.poster_pixels / poster.poster_pixels.max())
# # ax.imshow(poster.ambient_occlusion)
# plt.show()
# # # %%

#%%
ambient_occlusion = np.repeat(poster.ambient_occlusion[:, :, np.newaxis], 3, axis=2)
height_map = np.repeat(poster.height_map[:, :, np.newaxis], 3, axis=2)

direct_lighting = np.clip(np.sum(poster.normal_map * poster.lighting_vector, axis=2), 0, 1)
direct_lighting = np.repeat(direct_lighting[:, :, np.newaxis], 3, axis=2)

cast_shadow = np.clip(poster.cast_shadow, 1, 2) *255*0.5
cast_shadow = gaussian_filter(cast_shadow, sigma=poster.resolution[1]/100)

poster_pixels = np.repeat(cast_shadow[:, :, np.newaxis], 3, axis=2)

poster_pixels[height_map != 0] = (poster.color_map[height_map != 0] 
                                * direct_lighting[height_map != 0] 
                                * ambient_occlusion[height_map != 0])

poster_pixels *= 1.5
# poster_pixels = poster.color_map * direct_lighting * ambient_occlusion
poster_pixels = np.clip(poster_pixels, 0, 300)

poster.save_image(poster.cast_shadow, 'cast_shadow')
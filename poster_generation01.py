#%%
import matplotlib
matplotlib.use('qt5agg')  # Or use 'tkagg' if 'qt5agg' doesn't work
import matplotlib.pyplot as plt

from Poster import Poster

#%%
poster = Poster([200, 100])
poster.render()
print('Saving image')
poster.save_image()

#%% Save the different layers of the poster for debugging
poster.save_image(poster.ambient_occlusion, 'ambient_occlusion')
# poster.save_image(poster.altitude_map, 'altitude_map')
poster.save_image(poster.color_map, 'color_map')
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

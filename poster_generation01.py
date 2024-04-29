#%%
import matplotlib.pyplot as plt

from Poster import Poster

poster = Poster([100, 50])

# poster.globes.append(Globe(plate_index = 1)) 

poster.render()
poster.save_image()

#%%
# plt.figure(3)
# #plt.imshow(poster.masks.masks, cmap='gray')
# # plt.imshow(poster.poster_pixels[:,:,2]-poster.poster_pixels[:,:,0]-poster.poster_pixels[:,:,1]) #water filter
# plt.imshow(poster.ambient_occlusion.T, cmap='gray', alpha=0.5, vmin=-0.3, vmax=0.3)
# # plt.imshow(poster.height_map.T, cmap='jet', alpha=0.5)
# plt.show()

# #%%
# plt.figure(4)
# normal_map = poster.globes[1].altitude_map
# plt.imshow(normal_map.T)
# # plt.imshow(poster.height_map, cmap='jet', alpha=0.5)
# plt.show()

# #%%

#%%
import matplotlib.pyplot as plt

from Poster import Poster

poster = Poster([120, 60])

# poster.globes.append(Globe(plate_index = 1)) 

poster.render()
poster.save_image()
# poster.save_image(poster.ambient_occlusion)

#%%
plt.figure(3)
#plt.imshow(poster.masks.masks, cmap='gray')
# plt.imshow(poster.poster_pixels[:,:,2]-poster.poster_pixels[:,:,0]-poster.poster_pixels[:,:,1]) #water filter
plt.imshow(poster.ambient_occlusion.T, cmap='gray', alpha=0.5)
# plt.imshow(poster.height_map.T, cmap='jet', alpha=0.5)
plt.show()

plt.imshow(poster.direct_lighting.T, cmap='gray', alpha=0.5)
plt.show()
plt.imshow(poster.color_map.T, cmap='gray', alpha=0.5)
plt.show()

# #%%
# plt.figure(4)
# normal_map = poster.globes[1].altitude_map
# plt.imshow(normal_map.T)
# # plt.imshow(poster.height_map, cmap='jet', alpha=0.5)
# plt.show()

# #%%

# Ideas:
# Make light from cities in the shadow parts of the globes
# make the save function be flexible for different layers. 
# Save the poster here, but also be able to save the layers separately.
#%%
import matplotlib.pyplot as plt

from Poster import Poster

poster = Poster([120, 60])
poster.render()
poster.save_image()

#%%
plt.figure(3)
plt.imshow(poster.ambient_occlusion.T, cmap='gray', alpha=0.5)
plt.show()


# Ideas:
# Make light from cities in the shadow parts of the globes
# make the save function be flexible for different layers. 
# Save the poster here, but also be able to save the layers separately.
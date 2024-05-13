#%%
from Poster import Poster

poster = Poster([60, 30])
poster.render()
print('Saving image')
poster.save_image()

#%% Save the different layers of the poster for debugging
poster.save_image(poster.ambient_occlusion, 'ambient_occlusion')
poster.save_image(poster.altitude_map, 'altitude_map')
poster.save_image(poster.color_map, 'color_map')
poster.save_image(poster.normal_map,'normal_map')
poster.save_image(poster.height_map, 'height_map')
poster.save_image(poster.direct_lighting, 'direct_lighting')

# Ideas:
# Make light from cities in the shadow parts of the globes

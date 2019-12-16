import numpy as np

def maxproject_3c(image_3c):
    # This function takes a 3 channel image with multiple zplanes and max projects each of the 
    # planes into a singal image (ex, max_mCherry, max_GFP, max_DAPI)
    c0 = image_3c[..., 0]
    c1 = image_3c[..., 1]
    c2 = image_3c[..., 2]

    max_c0 = np.max(c0, axis = 2)
    max_c1 = np.max(c1, axis = 2)    
    max_c2 = np.max(c2, axis = 2)
    
    return np.stack((max_c0, max_c1, max_c2), axis = 2)
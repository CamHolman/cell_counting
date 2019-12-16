import numpy as np
import scipy as sp

def median_filt_3c(image_3c, size_kernel = 3):
    c0 = image_3c[..., 0]
    c1 = image_3c[..., 1]
    c2 = image_3c[..., 2]

    med_c0 = sp.signal.medfilt(c0, kernel_size = size_kernel)
    med_c1 = sp.signal.medfilt(c1, kernel_size = size_kernel)    
    med_c2 = sp.signal.medfilt(c2, kernel_size = size_kernel)

    return np.stack((med_c0, med_c1, med_c2), axis = 2)
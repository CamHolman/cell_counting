import numpy as np
import skimage as sk
from src.data.bioformats_importer import bioformats_importer
from src.data.maxproject_3c import maxproject_3c
from src.data.median_filt_3c import median_filt_3c


def x4_preprocess_image(image_path):
    img, meta = bioformats_importer(image_path)
    img_max = maxproject_3c(img)
    img_despec = median_filt_3c(img_max, size_kernel= 3)

    return img_despec, meta

import pandas as pd
import skimage as sk
import numpy as np
import os


def clob_to_dict(clob):
        return {
            'id': clob.id,
            'name': os.path.basename(clob.name)[:-4],
            #'image': clob.image,
            #'blobs': clob.blobs,
            #'pixels_per_micron': clob.pixels_per_micron,
            'num_cells': clob.num_cells,
            #'im_area': clob.im_area,
            'slice_area': clob.slice_area,
            'cells_per_um2': clob.cells_per_um2,
            'cells_per_mm2': clob.cells_per_mm2,
            'percent_slice': clob.percent_slice  
        }

def extract_panda(clob_list):
    dictlist = []
    for i in range(len(clob_list)):
        dictlist += [clob_to_dict(clob_list[i])]
    DF = pd.DataFrame(dictlist)
    return DF

def merge_counts(man_counts, clob_list):
    DF = extract_panda(clob_list)
    mDF = pd.merge(DF, man_counts, on='name' )
    return mDF
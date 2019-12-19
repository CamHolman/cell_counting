import pandas as pd
import skimage as sk
import numpy as np
import cc.count.countcells as cc
import os


default_ranges = {
    'max_sigma_min': 20,
    'max_sigma_max': 40,
    'num_sigma_min': 5,
    'num_sigma_max': 15
    'thresh_min': 0.01,
    'thresh_max': 0.3
}

def clob_to_dict(clob):
        return {
            'name': os.path.basename(clob.name)[:-4],
            #'image': clob.image,
            #'blobs': clob.blobs,
            #'pixels_per_micron': clob.pixels_per_micron,
            'num_cells': clob.num_cells,
            #'im_area': clob.im_area,
            #'slice_area': clob.slice_area,
            #'cells_per_area': clob.cells_per_area,
            #'percent_slice': clob.percent_slice  
        }

def merge_counts(man_counts, clob_list):
    dictlist = []
    for i in range(len(clob_list)):
        dictlist += [clob_to_dict(clob_list[i])]
    DF = pd.DataFrame(dictlist)
    mDF = pd.merge(DF, man_counts, on='name' )
    return mDF

def run_and_merge(
    man_counts, 
    imdir,
    log_params, 
    testi = 0, 
    verbose = False, ):
    """
    Run couting with set of log params, combine with manual
    counts, anad return pandas dataframe with both together    
    """

    ch_counts = cc.collect_cell_counts(
        imdir,
        log_params = log_params,  
        testi = testi, 
        verbose = verbose) 


    

def find_pearsons(man_counts, imdir, ranges=default_ranges):
    
    
    for sig in range



mDF = pd.merge(dfCH87, dfAC87, on='name' )
mDF


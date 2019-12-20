import pandas as pd
import skimage as sk
import numpy as np
from numpy import arange
import cc.count.countcells as cc
import os
from scipy.stats import pearsonr



def clob_to_dict(clob):
        return {
            'id': clob.id,
            #'name': os.path.basename(clob.name)[:-4],
            #'image': clob.image,
            #'blobs': clob.blobs,
            #'pixels_per_micron': clob.pixels_per_micron,
            'num_cells': clob.num_cells,
            #'im_area': clob.im_area,
            #'slice_area': clob.slice_area,
            #'cells_per_um2': clob.cells_per_um2,
            #'cells_per_mm2': clob.cells_per_mm2,
            #'percent_slice': clob.percent_slice  
        }

def extract_panda(clob_list):
    dictlist = []
    for i in range(len(clob_list)):
        dictlist += [clob_to_dict(clob_list[i])]
    DF = pd.DataFrame(dictlist)
    return DF

def merge_counts(man_counts, clob_list):
    DF = extract_panda(clob_list)
    mDF = pd.merge(DF, man_counts, on='id' )
    return mDF

def find_pearson(man_df, imdir, log_params):
    """
    man_df = pandas df of manual counts
    imdir = directory containing training images that have also been counted
    log_parames = parameters for laplacian of gaussian function
    """
    
    clobs = cc.collect_cell_counts(
        image_directory= imdir,
        log_params = log_params,
        testi=0,
        verbose = False,
        pixels_per_micron= 1.5
    )
    auto_df = extract_panda (clobs)
    merge_df = pd.merge(man_df, auto_df, on='id', how ='inner') 
    pearson = pearsonr (merge_df['man_count'], merge_df['num_cells'])
    return pearson



default_ranges = {
    'min_sigma_low': 1,
    'min_sigma_high': 10,
    'min_sigma_interval':1,
    'max_sigma_low': 20,
    'max_sigma_high': 80,
    'max_sigma_interval': 1,
    'num_sigma_low': 5,
    'num_sigma_high': 40,
    'num_sigma_interval': 1,
    'thresh_low': 0.01,
    'thresh_high': 0.5,
    'thresh_interval': 0.01,
    'overlap_low': 0.01,
    'overlap_high': 0.2,
    'overlap_interval': 0.01
}    

def train_cc(man_counts, imdir, ranges=default_ranges):
    collection = [ ]
    idx = 0

    for min_sigma in range(
                        ranges['min_sigma_low'],
                        ranges['min_sigma_high'],
                        ranges['min_sigma_interval']):
        for max_sigma in range(
                            ranges['max_sigma_low'],
                            ranges['max_sigma_high'],
                            ranges['max_sigma_interval']):
            for num_sigma in range(
                                ranges['num_sigma_low'],
                                ranges['num_sigma_high'],
                                ranges['num_sigma_interval']):
                for thresh in arange(
                                    ranges['thresh_low'],
                                    ranges['thresh_high'],
                                    ranges['thresh_interval']):
                    for overlap in arange(
                                        ranges['overlap_low'],
                                        ranges['overlap_high'],
                                        ranges['overlap_interval']):
                        
                        
                        if idx%10 == 0:
                            print("Trying combination #:", idx)
                        idx += 2
                        
                        log_params_1 = {
                            'min_s': min_sigma,
                            'max_s': max_sigma,
                            'num_s': num_sigma,
                            'thresh': thresh,
                            'overlap': overlap,
                            'log_scale': False,
                            'exclude_border': False
                        }     

                        log_params_2 = {
                            'min_s': min_sigma,
                            'max_s': max_sigma,
                            'num_s': num_sigma,
                            'thresh': thresh,
                            'overlap': overlap,
                            'log_scale': True,
                            'exclude_border': False
                        }                            

                        pearson1 = find_pearson(man_counts, imdir, log_params_1)

                        pearson2 = find_pearson(man_counts, imdir, log_params_2)

                        collection.append({
                            'pearson': pearson1,
                            'log_params': log_params_1,
                        })

                        collection.append({
                            'pearson': pearson2,
                            'log_params': log_params_2,
                        })

    return collection


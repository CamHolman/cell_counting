import skimage as sk
import os
from src.data.x4_preprocess_image import x4_preprocess_image

def x4_preprocess_batch_images(input_dir, output_dir = None):
    images = sk.io.ImageCollection(os.path.join(input_dir, '*.czi'))
    # print (images.files)

    im_list = [] 

    for i in range(len(images.files)):
        print ('Current Index in Batch Function =', i)

        image_path = images.files[i]
        image_name = os.path.basename(image_path)[:-4]

        pp_image, meta =  x4_preprocess_image(image_path)
        
        # Cana't dave OMEXML as meta directly, need to work on a change to mapping
        #sk.external.tifffile.imsave(output_dir + image_name + ".tif", pp_image, metadata = meta)
        
        sk.external.tifffile.imsave(output_dir + image_name + ".tif", pp_image, 'imagej')
        im_list.append([pp_image, meta])

    return im_list


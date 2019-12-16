import javabridge
import bioformats
import numpy as np
import matplotlib.pyplot as plt 



def bioformats_importer(image_path):
    # Start javabridge
    # Keeping javabridge start in funciton for now - double check if problems arise
    javabridge.start_vm(class_path=bioformats.JARS)
    
    # Get Image
    im_clob = bioformats.ImageReader(image_path)
    image_0 = im_clob.read(z = 0, rescale = False)
    image_1 = im_clob.read(z = 1, rescale = False)
    image_2 = im_clob.read(z = 2, rescale = False)
    image = np.stack((image_0, image_1, image_2), axis = 2)
    
    # Get Metadata 
    meta_clob = bioformats.get_omexml_metadata(image_path)
    meta = bioformats.OMEXML(meta_clob)

    # Kill Javabridge
    # Moved 
    # This is being moved to the script (outside function).
    # Due to a limitation of Java, bridge can only be opened
    # once per kernel, closing and reopening for each image does not work
    ### javabridge.kill_vm()

    return image, meta



import matplotlib.pyplot as plt 

def plot_3c(image):
    print ('Shape: ', image.shape)
    print ('Type:', type(image))
    print ('Dtype:', image.dtype)

    fig, (ax0, ax1, ax2) = plt.subplots(1,3, figsize = (30,10))
    ax0.imshow(image[...,0])
    ax1.imshow(image[...,1])
    ax2.imshow(image[...,2])

    return fig
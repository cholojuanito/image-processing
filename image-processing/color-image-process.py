# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'image-processing'))
	print(os.getcwd())
except:
	pass
#%%
from IPython import get_ipython

#%% [markdown]
# # Image Processing Lab
# All  of  the  programming  assignments  are  to  be  done  in  Python  using  additional  libraries  specified  in  the  assignments.  There  are many  libraries  available,  some  of  which  we  will  be  using,  and  you  are  welcome  to  use  them  with  one  exception:  if  the  library  or  a  function  within  it  performs  the  specific  function  you  are  asked  to  code,  you  may  not  use  that  other  than  perhaps  as  a  reference  to  compare  against. All  of  the  code  you  submit  must  be  your  own. You are welcome to turn in a completed jupyter notebook.
#%% [markdown]
# The following code will load an image you can use for this lab. If needed make sure to install PIL using *pip install PIL* or *conda install PIL*.
#%% [markdown]
# ## Pre-lab Notes
# Since it is our first time working with color images, we need to be careful of a couple of things. Most RGB color images store each RGB value as an 8-bit number. This is fine for displaying images as shown below:

#%%
from imageio import imread
import matplotlib.pyplot as plt
import numpy as np
import time

racoon = imread('racoon.jpg')
plt.imshow(racoon); plt.show()

#%% [markdown]
# This is fine for displaying, but becomes a problem once we try to do any image manipulations. We have to beware of overflow. For example, lets say we just want to add 20 to all of the RGB values.

#%%
plt.imshow(racoon + 20)
plt.show()

#%% [markdown]
# Notice what happens near the white areas of the image. We only had 8-bits to respresent each RGB value (0 to 255). White areas will have values near 255. So when we add 20, the colors go crazy because values have overflowed (ex. 240 + 20 = 4).
# 
# You maybe tempted to try something like this:

#%%
plt.imshow(np.minimum(racoon + 20, 255))
plt.show()

#%% [markdown]
# Notice that this still doesn't work because the overflow occurs before the maximum check.
# 
# The way to beat this problem is to convert the image into a higher bit representation, do the manipulations, then convert it back down to the 8-bit representation.

#%%
racoon_32 = np.array(racoon, dtype=np.int32)
racoon_32 = np.minimum(racoon_32 + 20, 255)
racoon_8 = np.array(racoon_32, dtype=np.uint8)

plt.imshow(racoon_8)
plt.show()

#%% [markdown]
# For convenience, we will leave all data in int32 representation. Then, we will simply define a function that converts the image back to 8-bit representation before plotting.

#%%
def plotImage(image, title="", cmap=None):
    im = np.array(image, dtype=np.uint8)
    plt.imshow(im, vmin = 0, vmax = 255, cmap=cmap)
    plt.title(title)
    plt.show()

racoon = imread('racoon.jpg')
racoon = np.array(racoon, dtype=np.int32)
plotImage(racoon)

#%% [markdown]
# You are welcome to use the function above for plotting your own color images.
# 
# In this lab, you will also need to be able to convert between RGB values and HSB values. We have provided functions that allow you to easily go back and forth while staying in the 0-255 representation for images. You are welcome to use the functions below in this lab.

#%%
def toHSB(image):
    from matplotlib import colors
    temp = 255*colors.rgb_to_hsv(image/255.0)
    return temp.astype(np.int32)
    
def toRGB(image):
    from matplotlib import colors
    temp = 255*colors.hsv_to_rgb(image/255.0)
    return temp.astype(np.int32)

#%% [markdown]
# Now that you have that understanding, you are ready to start the lab.
# 
# Implement each of the following functions. Use the provided test cases to test your functions.
#%% [markdown]
# ## Function 1: Convert to grayscale
# Takes in a color image and returns a grayscale image using the following formula: Gray = 0.299 Red + 0.587 Green + 0.114 Blue

#%%
def toGrayScale(image):
    # I used the luminosity method found here https://en.wikipedia.org/wiki/Grayscale
    gray_value_constants = [0.2126, 0.7152, 0.0722] #RGB to grayscale constants
    return np.dot(image[..., :], gray_value_constants)


#%%
# Test Case
gray_racoon = toGrayScale(racoon)
plotImage(gray_racoon, "Gray Racoon", "gray")

#%% [markdown]
# ## Function 2: Brightness Adjustment
# Takes in a color image and returns the brightened version of that image according to a passed in parameter. Use a max image value of 255.

#%%
def brightAdjust(image,c):
    im = toHSB(image)
    # Add the brightness value to the index that corresponds to "B" in HSB
    im[... ,2] += c
    return toRGB(np.clip(im, 0, 255))


#%%
# Test Case
bright_racoon = brightAdjust(racoon,100)
plotImage(bright_racoon, "Bright Racoon")
dark_racoon = brightAdjust(racoon,-100)
plotImage(dark_racoon, "Dark Racoon")

#%% [markdown]
# ## Function 3: Contrast Adjustment
# Takes in a color image and returns the contrasted version of that image according to a passed in parameter. Use a max image value of 255.
# 
# Also, rather than a straight linear operation, we will use a mapping similar to what Photoshop does. In particular, the contrast will be in the range [-100,100] where 0 denotes no change, -100 denotes complete loss of contrast, and 100 denotes maximum enhancement (8x multiplier). If *c* is the contrast parameter, then the level operation applied is:
# 
# $$s = \left(\frac{c+100}{100}\right)^4 (r-128) + 128$$
# 
# Make sure you work in floating point, not integers. Integer division would not be very acurate.

#%%
def contrastAdjust(image, c):
    image = toHSB(image)

    image[...,2] = ((((c + 100.0) / 100.0) **4.0) * (image[...,2] - 128)) + 128

    return toRGB(np.clip(image, 0, 255))


#%%
contrast_racoon = contrastAdjust(racoon,30)
plotImage(contrast_racoon, "High Contrast Racoon")

#%% [markdown]
# ## Function 4: Image Blending
# Takes in 2 color images of the same size. Given an alpha value it returns the blended image according to the alpha value. Note that your alpha value can be a single number or a mask image of the same size. The alpha values will be between 0 and 1.

#%%
def alphaBlend(image1, image2, alpha = .5):
    return np.clip(alpha*image1+(1-alpha)*image2, 0, 255)


#%%
# Test Cases
man = imread("man.jpg")
city = imread("city.jpg")
blended = alphaBlend(man, city, .7)
plotImage(blended, "Alpha Blend with Single Value")

mask1 = imread("alphamask1.jpg")/255.0
blended1 = alphaBlend(man, city, mask1)
plotImage(blended1, "Alpha Blend with Mask 1")

beach = imread("beach.jpg")
boat = imread("boat.jpg")
mask2 = imread("alphamask2.jpg")/255.0
blended2 = alphaBlend(boat, beach, mask2)
plotImage(blended2, "Alpha Blend with Mask 2")

#%% [markdown]
# ## Function 5: Cross Dissolve
# 
# Takes in 2 color images of the same size. Returns an array of alpha blend of those two images, where the first picture is an alpha value of 1, the last picture is an alpha value of 0, and the middle pictures slowly decrease until reaching zero. Allow the user to specify the number of steps in the cross dissolve. You can then feed this array into our animation function to view the cross dissolve.

#%%
def crossDissolve(image1, image2, numsteps = 10):
    imgs = []
    value = 1
    step_amt = 1 / numsteps
    
    for i in range(numsteps):
        imgs.append(alphaBlend(image1, image2, value))
        value -= step_amt
    
    return imgs


#%%
#Test Case
import matplotlib.animation as animation
get_ipython().run_line_magic('matplotlib', 'notebook')

beach = imread("beach.jpg")
boat = imread("boat.jpg")
dis = crossDissolve(beach, boat)

fig = plt.figure()
ims = []
for im in dis:
    im = np.array(im, dtype=np.uint8)
    result = plt.imshow(im, vmin=0, vmax=255, animated=True)
    ims.append([result])

ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True)
plt.show()

#%% [markdown]
# Because we are working in a notebook, this may not display properly. If necessary, plot the individual pictures to verify that the cross dissolve is working. Also, run the following line of code once you are done to return back to normal plotting functions.

#%%
get_ipython().run_line_magic('matplotlib', 'inline')

#%% [markdown]
# ## Function 6: Uniform Blurring
# Takes in a grayscale image and returns a corresponding result that has been blurred (spatially filtered) using a uniform averaging. Allow the user to specify the size of the kernel (ex. size=3 would give a 3x3 kernel). You can ignore the edge pixels. (Hint: np.sum() may be useful)
           

#%%
def blur(image,size=3):
    # Create a result buffer so that you don't affect the original image
    result = np.zeros(image.shape)
    offset = int(size / 2)
    h, w = result.shape

    ##Creates an array of the neighboring pixels
    neighborhood = lambda y, x : [image[y2][x2] 
        for y2 in range(y-offset, y+offset+1) 
            for x2 in range(x-offset, x+offset+1)
                if (-1 < x < w and -1 < y < h and
                   0 <= x2 < w and 0 <= y2 < h)]
    
    for y in range(h):
        for x in range(w):
             result[y,x] = np.sum(neighborhood(y, x))/size**2
    
    return result
    


#%%
# Test Cases

gray_racoon = toGrayScale(racoon)
start_time1 = time.time()
blur_racoon = blur(gray_racoon)
end_time1 = time.time()
plt.imshow(blur_racoon,cmap="Greys_r",vmin=0,vmax=255); plt.title("Uniform Blurring")
plt.show()

start_time2 = time.time()
blur_racoon2 = blur(gray_racoon, 7)
end_time2 = time.time()
plt.imshow(blur_racoon2,cmap="Greys_r",vmin=0,vmax=255); plt.title("Uniform Blurring (7x7)")
plt.show()

print(f'Time1: {end_time1 - start_time1} seconds')
print(f'Time2: {end_time2 - start_time2} seconds')

#%% [markdown]
# ## Function 7: Median Filter
# Takes in a grayscale image and returns a corresponding result that has been median filtered. Allow the user to specify the size of the kernel (ex. size=3 would give a 3x3 kernel). You can ignore the edge pixels.

#%%
def medianFilter(image,size=3): #Must be odd?
    result = np.zeros(image.shape)
    offset = int(size / 2)
    h, w = result.shape

    #Creates a numpy array of the neighboring pixels
    neighborhood = lambda y, x : [image[y2][x2]
        for y2 in range(y-offset, y+offset+1)  
            for x2 in range(x-offset, x+offset+1)
                if (-1 < x < w and -1 < y < h and
                   0 <= x2 < w and 0 <= y2 < h)]
    
    for y in range(h):    
        for x in range(w):
             result[y,x] = np.median(neighborhood(y, x))

    return result


#%%
# Test Cases
gray_racoon = toGrayScale(racoon)
start_time1 = time.time()
median_racoon = medianFilter(gray_racoon)
end_time1 = time.time()
plt.imshow(median_racoon,cmap="Greys_r",vmin=0,vmax=255); plt.title("Median Blurring")
plt.show()

start_time2 = time.time()
median_racoon2 = medianFilter(gray_racoon, 7)
end_time2 = time.time()
plt.imshow(median_racoon2,cmap="Greys_r",vmin=0,vmax=255); plt.title("Median Blurring (7x7)")
plt.show()

print(f'Time1: {end_time1 - start_time1} seconds')
print(f'Time2: {end_time2 - start_time2} seconds')

#%% [markdown]
# ## Function 8: General Convolution
# 
# Now that you have written a couple of different kernels, write a general convolution function that takes in an image and kernel (stored as a numpy matrix), and performs the appropriate convolution. You can assume the kernel is 3x3 if you would like, but it is not much harder to do a general size kernel as well.

#%%
def convolution(image,kernel):
    result = np.zeros_like(image)
    offset = int(kernel.shape[0] / 2)
    h, w = result.shape

    #Creates a numpy array of the neighboring pixels
    neighborhood = lambda y, x: [image[y2][x2] 
        if (-1 < x < w and -1 < y < h and
            0 <= x2 < w and 0 <= y2 < h)
        else 0
            for x2 in range(x-offset, x+offset+1) 
                for y2 in range(y-offset, y+offset+1)]
    
    for y in range(h):
        for x in range(w):
            result[y,x] = np.sum((np.multiply(kernel, np.reshape(neighborhood(y,x), kernel.shape))))
    return result


#%% [markdown]
# To make sure your general convolution is working, compare the following test case with your original blur results.

#%%
# Test Cases
gray_racoon = toGrayScale(racoon)

blur_kernel = np.matrix([[1, 1, 1],
                        [1, 1, 1],
                        [1, 1, 1]])

blur_racoon2 = convolution(gray_racoon, blur_kernel)/9.0
plt.imshow(blur_racoon2,cmap="Greys_r",vmin=0,vmax=255); plt.title("Uniform Bluring")
plt.show()

#%% [markdown]
# ## Function 9: Sharpening
# Takes in a grayscale image and returns a corresponding result that has been sharpened using an unsharp masking kernel that has a 6 in the middle and -1s for the four-connected neighbors. You can use your general convolution function. You can ignore the edge pixels. **Don't forget to normalize your results.**

#%%
def sharpen(image):
    kernel = np.array([[1, -1, 1],
                       [-1, 6, -1],
                       [1, -1, 1]])
    return convolution(image,kernel)/kernel.shape[0]**2


#%%
# Test Cases
gray_racoon = toGrayScale(racoon)
sharpen_racoon = sharpen(gray_racoon)
plt.imshow(sharpen_racoon,cmap="Greys_r",vmin=0,vmax=255); plt.title("Sharpened")
plt.show()

#%% [markdown]
# ## Function 10: Edge Detection
# Takes in a grayscale image and returns a corresponding result that shows the gradient magnitude of the input. Use a Sobel kernel. You may afterward scale the result for visibilty if you wish when you demonstrate the function. You can use your general convolution function. You can ignore the edge pixels.

#%%
def edgeDetect(image):
    from math import sqrt
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])
    kernel_y = np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]])

    img_x = convolution(image, kernel_x)/8
    img_y = convolution(image, kernel_y)/8

    h,w = image.shape
    result = np.zeros_like(image)

    for y in range(h):
        for x in range(w):
            result[y,x] = sqrt((img_x[y][x]**2)+(img_y[y][x]**2))

    return result


#%%
# Test Cases
gray_racoon = toGrayScale(racoon)
edge_racoon = edgeDetect(gray_racoon)
plt.imshow(edge_racoon,cmap="Greys_r",vmin=0,vmax=255); plt.title("Edge Detection")
plt.show()


#%%




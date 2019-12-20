# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'image-warping'))
	print(os.getcwd())
except:
	pass
# %% [markdown]
# # Image Warping Lab
# %% [markdown]
# ## Part 1: Interpolation
# 
# Since we are going to be warping images, we need to make sure we have a good interpolation function to deal with inexact pixel locations.
# 
# In the cell below, we want to scale an image by a factor of 2.30 in both x and y. **Write a function called "interpolate" that performs bilinear interpolation.** This function should take in the image and a location (x,y) of interest. It then uses the nearby pixels to that location to interpolate and return an RGB value.

# %%
from imageio import imread, imsave
import matplotlib.pyplot as plt
import numpy as np
import math

#Your bilinear interpolation function
def interpolate(image, x, y):
    top_l = np.zeros(3)
    top_r = np.zeros(3)
    bot_l = np.zeros(3)
    bot_r = np.zeros(3)
    h = math.floor(x)
    w = math.floor(y)
    
    if h < len(image) - 1 and w < len(image[0]) - 1:
        top_r = image[h+1, w+1]
    else:
        top_r = image[h,w]
    if h < len(image) - 1 and w > 1:
        top_l = image[h+1, w]
    else:
        top_l = image[h,w]
        
    if w < len(image[0]) - 1 and h > 1:
        bot_r = image[h, w+1]
    else:
        bot_r = image[h,w]
    if w > 1 and h > 1:
        bot_l = image[h, w]
    else:
        bot_l = image[h,w]
    
    X = x-h
    Y = y-w

    left_val = (bot_l*(1-X))+(top_l*X)
    right_val = (bot_r*(1-X))+(top_r*X)

    return (left_val*(1-Y))+(right_val*Y)



filename = "test.png"
im = imread(filename)

h,w,_ = im.shape
scale = 2.3

result = np.zeros((int(scale*h),(int(scale*w)),3), dtype="uint8")

result[0:h,0:w,:] = im #Temporary line, you can delete it

#Write code that scales the image by a factor of 2.3
#It should call interpolate.


for x in range(int(scale*h)):
    for y in range(int(scale*w)):
        result[x,y] = interpolate(im,x/scale,y/scale)

        
plt.imshow(result,vmin=0)
plt.show()

# %% [markdown]
# ## Part 2: Backwards Mapping
# 
# Now that we have a interpolation function, we need a function that performs a backward mapping between a source and target image.
# 
# Given a simple rotation transformation, **write a function that performs a backwards mapping. This function should also call your interpolate function.**
# 
# For this example, the source and target image will be the same size, which means part of your rotated image will be cut off on the corners. You can assume that all pixels need to be backward mapped. Also, **don't forget to invert the transform. This is really easy in numpy.**

# %%
def backmap1(image, transform):
    
    h,w,_ = im.shape
    
    result = np.zeros((h,w,3), dtype="uint8")
    inv = np.asarray(np.linalg.inv(transform))


    for x in range(h):
        for y in range(w):
            pt = np.dot(inv, np.array([x,y,1]))
            if 0 < pt[0] < h and  0 < pt[1] < w :
                result[x,y] = interpolate(image, pt[0], pt[1])

    return result


from math import sin,cos,pi

filename = "test.png"
im = imread(filename)

transform = np.matrix([[cos(45 * pi/180), -sin(45 * pi/180), w/2],[sin(45 * pi/180),cos(45 * pi/180),-h/5],[0,0,1]])

result = backmap1(im,transform)

plt.imshow(result,vmin=0)
plt.show()

# %% [markdown]
# ## Part 3: Homographies
# 
# Now that we have the two specific functions that we need, let's start looking at some more interesting image warping. In class, we discussed how we can use homographies to warp images nonlinearly. In this lab, we have provided the homography generating code for you. 

# %%
class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y


def getHomography(s0,s1,s2,s3,t0,t1,t2,t3):

    x0s = s0.x
    y0s = s0.y
    x0t = t0.x
    y0t = t0.y

    x1s = s1.x
    y1s = s1.y
    x1t = t1.x
    y1t = t1.y

    x2s = s2.x
    y2s = s2.y
    x2t = t2.x
    y2t = t2.y

    x3s = s3.x
    y3s = s3.y
    x3t = t3.x
    y3t = t3.y

    #Solve for the homography matrix
    A = np.matrix([
            [x0s, y0s, 1, 0, 0, 0, -x0t*x0s, -x0t*y0s],
            [0, 0, 0, x0s, y0s, 1, -y0t*x0s, -y0t*y0s],
            [x1s, y1s, 1, 0, 0, 0, -x1t*x1s, -x1t*y1s],
            [0, 0, 0, x1s, y1s, 1, -y1t*x1s, -y1t*y1s],
            [x2s, y2s, 1, 0, 0, 0, -x2t*x2s, -x2t*y2s],
            [0, 0, 0, x2s, y2s, 1, -y2t*x2s, -y2t*y2s],
            [x3s, y3s, 1, 0, 0, 0, -x3t*x3s, -x3t*y3s],
            [0, 0, 0, x3s, y3s, 1, -y3t*x3s, -y3t*y3s]
        ])

    b = np.matrix([
            [x0t],
            [y0t],
            [x1t],
            [y1t],
            [x2t],
            [y2t],
            [x3t],
            [y3t]
        ])

    #The homorgraphy solutions a-h
    solutions = np.linalg.solve(A,b)

    solutions = np.append(solutions,[[1.0]], axis=0)

    #Reshape the homography into the appropriate 3x3 matrix
    homography = np.reshape(solutions, (3,3))
    
    return homography

def getScreen():
    result = []
    screen = np.loadtxt("screen.txt")
    for line in screen:
        result.append(Point(int(line[0]), int(line[1])))
    return result

# %% [markdown]
# We want to be able to get a new image into the tv set in the image shown below. Note that not all pixels will need to be backward mapped. For this reason, we also need to specify a list of points that we are considering. This is provided in the getScreen function definined above.
# 
# **Rewrite your backmap function to allow for two images of different sizes and a specific set of points that need to be mapped.**

# %%
def backmap2(source, target, transform, points):
    h,w,_ = target.shape
    result = np.copy(target)
    inv = np.asarray(np.linalg.inv(transform))

    for pt in points:
        new_pt = np.dot(inv, np.array([pt.x, pt.y, 1]))
        if 0 < new_pt[0] < h and  0 < new_pt[1] < w :
                result[pt.y, pt.x] = interpolate(source, new_pt[1], new_pt[0])

    return result



filename = "test.png"
im = imread(filename)

h,w,_ = im.shape
        
s0 = Point(0,0)
s1 = Point(w-1,0)
s2 = Point(w-1,h-1)
s3 = Point(0,h-1)

t0 = Point(245,152)
t1 = Point(349,150)
t2 = Point(349,253)
t3 = Point(246,261)

tv = imread('tv.jpg')
plt.imshow(tv,vmin=0)
plt.show()

transform = getHomography(s0,s1,s2,s3,t0,t1,t2,t3)

screen = getScreen()

result = backmap2(im, tv, transform, screen)

plt.imshow(result,vmin=0)
plt.show()

# %% [markdown]
# ## Part 4: Geometric Tests
# 
# We have a pretty robust warping algorithm now, but we need a way of determining which pixels are of interest and which pixels are not of interest on our target image.
# 
# Notice in the image below that we were able to replace the nearest canvas with a picture of BYU campus. We did so by finding the corners of the canvas, determining points that lie inside that canvas, and then using a homography as our transform for the backward mapping. We left a blank canvas for you to try this out as well. 
# 
# **Rewrite your backmap function (yet again) to take in the corners of interest, perform a homography, and include a pixel tester that makes a bounding box around the area of interest, then uses cross product geometric testing to verify if a pixel is on the canvas** (we acknowledge there are other ways you could solve this problem, but this is good practice).
# 

# %%
def getCanvas(t0, t1, t2, t3):
    canvas = []

    for x in range(t3.x,t1.x):
        for y in range(t0.y, t3.y):
            canvas.append(Point(x,y))
    
    return canvas


def backmap3(source,target,s0,s1,s2,s3,t0,t1,t2,t3):
    points = getCanvas(t0, t1, t2, t3)
    transform = getHomography(s0,s1,s2,s3,t0,t1,t2,t3)

    h,w,_ = target.shape
    result = np.copy(target)
    inv = np.asarray(np.linalg.inv(transform))

    for pt in points:
        new_pt = np.dot(inv, np.array([pt.x, pt.y, 1]))
        if 0 < new_pt[0] < h and  0 < new_pt[1] < w :
                result[pt.y, pt.x] = interpolate(source, new_pt[1], new_pt[0])

    return result
    

museum = imread('museum.png')
plt.imshow(museum,vmin=0)
plt.show()

filename = "test.png"
im = imread(filename)

h,w,_ = im.shape
        
s0 = Point(0,0)
s1 = Point(w-1,0)
s2 = Point(w-1,h-1)
s3 = Point(0,h-1)

t0 = Point(268,230)
t1 = Point(349,249)
t2 = Point(347,361)
t3 = Point(267,363)

result = backmap3(im,museum,s0,s1,s2,s3,t0,t1,t2,t3)
    
plt.imshow(result,vmin=0)
plt.show()



# %%

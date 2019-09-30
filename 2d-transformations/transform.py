# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '2d-transformations'))
	print(os.getcwd())
except:
	pass
#%%
from IPython import get_ipython

#%% [markdown]
# # Image Transformations Lab
# All  of  the  programming  assignments  are  to  be  done  in  Python  using  additional  libraries  specified  in  the  assignments.  There  are many  libraries  available,  some  of  which  we  will  be  using,  and  you  are  welcome  to  use  them  with  one  exception:  if  the  library  or  a  function  within  it  performs  the  specific  function  you  are  asked  to  code,  you  may  not  use  that  other  than  perhaps  as  a  reference  to  compare  against. All  of  the  code  you  submit  must  be  your  own. You are welcome to turn in a completed jupyter notebook.
# 
# The following code will load an image you can use for this lab. If needed make sure to install PIL using *pip install PIL* or *conda install PIL*.
# 
# **Note:** On the homework, the direction of the positve Y-axis was up. In this lab (and most image packages), the direction of the positive Y-axis is down. This means that you will need to rotate in the opposite direction of what you did on the homework.

#%%
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

get_ipython().run_line_magic('matplotlib', 'notebook')

def compose(frame, image, transformation):
    
    width, height = frame.size
    
    #Invert matrix for compose function, grab values for Affine Transform
    t = np.linalg.inv(transformation)
    a=t[0,0]; b=t[0,1]; c=t[0,2]; d=t[1,0]; e=t[1,1]; f=t[1,2]
    
    image = image.transform((width,height), Image.AFFINE,(a,b,c,d,e,f), Image.BICUBIC)

    #Make mask from image's location
    im = np.sum(np.asarray(image), -1)
    vals = 255.0*( im > 0)
    mask = Image.fromarray(vals).convert("1")

    #Composite images together
    result = Image.composite(image,frame,mask)

    return result


#Open the two images
filename = "PictureFrameCollage.png"
frame = Image.open(filename).convert("RGB")

filename0 = "Bird0.png"
filename1 = "Bird1.png"
filename2 = "Bird2.png"
filename3 = "Bird3.png"
filename4 = "Bird4.png"
filename5 = "Bird5.png"
filename6 = "Bird6.png"
filename7 = "Bird7.png"
filename8 = "Bird8.png"
filename9 = "Bird9.png"
filename10 = "Bird10.png"
filename11 = "Bird11.png"

im = Image.open(filename0).convert("RGB")
im1 = Image.open(filename1).convert("RGB")
im2 = Image.open(filename2).convert("RGB")
im3 = Image.open(filename3).convert("RGB")
im4 = Image.open(filename4).convert("RGB")
im5 = Image.open(filename5).convert("RGB")
im6 = Image.open(filename6).convert("RGB")
im7 = Image.open(filename7).convert("RGB")
im8 = Image.open(filename8).convert("RGB")
im9 = Image.open(filename9).convert("RGB")
im10 = Image.open(filename10).convert("RGB")
im11 = Image.open(filename11).convert("RGB")

#Creates transformation matrices given the: 
# - scaling value
# - translation in x and y direction
# - angle of rotation
def transform(scale=1.0, translate=(0,0), angle=None):
    if angle is not None:
        from math import radians, cos, sin
        rads = radians(angle)
        return np.array([ [scale* cos(rads), scale*sin(rads), translate[0]],
                          [-scale*sin(rads), scale*cos(rads), translate[1]],
                          [0, 0, 1]
                        ])
    else:
        return np.array([ [scale, 0, translate[0]],
                          [0, scale, translate[1]],
                          [0, 0, 1]
                        ])

#Compose the images together
result = compose(frame, im, transform(scale=1, translate=(619, 433)))
result = compose(result, im1, transform(scale=1.25, translate=(41, 30)))
result = compose(result, im2, transform(scale=0.389, translate=(283, 46)))
result = compose(result, im3, transform(translate=(419, 87), angle=30))
result = compose(result, im4, transform(scale=0.653, translate=(673, 37), angle=-15))
result = compose(result, im5, transform(translate=(350, 138), angle=-45))
result = compose(result, im6, transform(translate=(385, 379), angle=45)) 
result = compose(result, im7, transform(scale=0.389, translate=(514, 225)))
result = compose(result, im8, transform(scale=0.736, translate=(633, 228),angle=15))
result = compose(result, im9, transform(scale=0.389, translate=(305, 358), angle=-45))
result = compose(result, im10, transform(scale=1.21, translate=(46, 354), angle=15))
result = compose(result, im11, transform(scale=0.736, translate=(308, 463)))
    
#Show the result
plt.imshow(result)
plt.show()

#Uncomment this line if you want to save the image
result.save("Output.png")

#%% [markdown]
# Tip: Make sure you are comfortable with building your own transformations and how the compositing code works, then try implementing your own general transform function.

#%%




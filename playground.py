"""
## Imports
"""

import cv2      
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


"""
### Method to split the image into blocks
"""

def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size
    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    assert h % nrows == 0, f"{h} rows is not evenly divisible by {nrows}"
    assert w % ncols == 0, f"{w} cols is not evenly divisible by {ncols}"
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))

"""
### Method to find prime numbers
"""

def SieveOfEratosthenes(num):
    prime = [True for i in range(num+1)]
    p = 2
    while (p * p <= num):
        if (prime[p] == True):
            # Updating all multiples of p
            for i in range(p * p, num+1, p):
                prime[i] = False
        p += 1
    
    return prime


"""
### Method to find GCDs of blocks
"""

def gcd(arr, isPrime):
    prev=arr[0]
    
    for i in range(1, len(arr)):
        if(isPrime[prev] and isPrime[arr[i]]):
            prev = prev - arr[i]
        elif(isPrime[prev] or isPrime[arr[i]]):
            if(arr[i]%prev==0):
                pass
            elif(prev%arr[i]==0):
                prev = arr[i]
            else:
                prev = prev - arr[i]
        else:
            prev = np.gcd(prev, arr[i])
    
    return prev


"""
## Method for Image Segmentation
"""

def segmentImage(matrix, th):
    r= len(matrix)
    c= len(matrix[0])
    rows, cols = (r, c)
    result = [[0 for i in range(cols)] for j in range(rows)]

    for i in range(0, r):
        for j in range(0, c):
            if(matrix[i][j]>=th):
                result[i][j]=255
            else:
                result[i][j]=0

    return result


"""
## Method to process individual channel of image
"""

def processImage(img, channel):
    # applying Otsu thresholding
    thresh, otsu_output = cv2.threshold(img, 120, 255, cv2.THRESH_OTSU)

    # dividing the image into 16 blocks
    blocks = blockshaped(img, len(img)//4, len(img[0])//4)

    # preprocessing the prime numbers
    isPrime = SieveOfEratosthenes(255)
    
    # finding GCDs of blocks
    gcds = []
    for i in range (0, len(blocks)):
        tmp=[]
        for j in range (0, len(blocks[i])):
            tmp.append(gcd(blocks[i][j], isPrime))
        gcds.append(gcd(tmp, isPrime))

    # finding Standard Deviation of GCDs of blocks
    # And segmenting image for Standard Deviation as threshold
    std = np.std(gcds)
    stdmatrix = segmentImage(img, std)

    # finding Mean of GCDs of blocks
    # And segmenting image for mean as threshold
    avg = np.mean(gcds)
    avgmatrix = segmentImage(img, avg)

    # finding Median of GCDs of blocks
    # And segmenting image for median as threshold
    med = np.median(gcds)
    medmatrix = segmentImage(img, med)

    results=[img, otsu_output, avgmatrix, medmatrix, stdmatrix]

    channel_name=""

    if(channel==0):
        channel_name="Red"
    elif(channel==1):
        channel_name="Green"
    else:
        channel_name="Blue"
    

# Creating thumbnail for image
imgpath="<path>"
image = Image.open(imgpath)
image.thumbnail((300, 200))
image.save('input1.png')

inputImage = Image.open("input1.png")
channels = Image.Image.split(inputImage)

np.array(channels[0]).shape

for i in range(0, 3):
    processImage(np.array(channels[i]), i)
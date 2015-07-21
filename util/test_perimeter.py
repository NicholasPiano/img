input_path = '/Volumes/transport/data/puzzle/050714-test/img/composite/050714-test_s13_ch-zbf-regions_t0_z0.tiff'

import numpy as np
from scipy.misc import imread
from skimage import exposure
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_erosion as erode
from scipy.ndimage.morphology import binary_dilation as dilate
from scipy.signal import find_peaks_cwt as find_peaks
from scipy.ndimage.measurements import center_of_mass as com
from scipy.ndimage.measurements import label
import scipy

def cut_to_black(array):
  # coordinates of non-black
  r0 = np.argmax(np.any(array, axis=1))
  r1 = array.shape[0] - np.argmax(np.any(array, axis=1)[::-1])
  c0 = np.argmax(np.any(array, axis=0))
  c1 = array.shape[1] - np.argmax(np.any(array, axis=0)[::-1])

  # return cut
  return array[r0:r1,c0:c1], (r0,c0,(r1-r0),(c1-c0))

def lin_fit(x, y, m0):
  '''Fits a linear fit of the form mx+b to the data'''
  fitfunc = lambda params, x: params[0] * x #create fitting function of form mx
  errfunc = lambda p, x, y: fitfunc(p, x) - y              #create error function for least squares fit

  init_a = m0                            #find initial value for a (gradient)
  init_p = np.array((init_a))  #bundle initial values in initial parameters

  #calculate best fitting parameters (i.e. m and b) using the error function
  p1, success = scipy.optimize.leastsq(errfunc, init_p.copy(), args = (x, y))
  f = fitfunc(p1, x)          #create a fit with those parameters
  return p1, f

img = imread(input_path)

L, n = label(img)

img1 = np.zeros(img.shape)
img1[L==1] = 255

img1 = erode(img1, iterations=20)

edge = img1 - erode(img1)
# print(np.sum(edge>0))

edge, (r0, c0, r1, c1) = cut_to_black(edge)

# for all edge pixels, do a 5x5 mask least squares fit and get R^2 for each one.
pixels = list(zip(np.where(edge)[0], np.where(edge)[1]))
pixel_set = set()

# edge_set = set()
# m0 = 0.628318
m0 = 0.5
mask_radius = 7
smallest_gradient = 1.0/(2*mask_radius)

lines = np.zeros(edge.shape)

for i, pixel in enumerate(pixels):
  # pixel = (0,5)
  rp, cp = pixel

  rb = 0 if pixel[0]-mask_radius-1 < 0 else pixel[0]-mask_radius-1
  re = edge.shape[0] if pixel[0]+mask_radius >= edge.shape[0] else pixel[0]+mask_radius
  cb = 0 if pixel[1]-mask_radius-1 < 0 else pixel[1]-mask_radius-1
  ce = edge.shape[1] if pixel[1]+mask_radius >= edge.shape[1] else pixel[1]+mask_radius

  # 1. get mask of pixels
  mask = edge[rb:re,cb:ce]

  # 2. get coordinates of original pixel
  rO, cO = pixel_coords = pixel[0] - rb, pixel[1] - cb # coordinates of original pixel with respect to mask

  # 3. shift all pixels to make original pixel the origin
  mask_pixels_r, mask_pixels_c = np.where(mask==1.0)[0] - pixel_coords[0], np.where(mask==1.0)[1] - pixel_coords[1]

  # 4. do least squares fitting, forcing gradient through origin
  p, f = lin_fit(mask_pixels_c, mask_pixels_r, m0) #
  m = (p[0] if abs(p[0])>smallest_gradient else 0) if p[0]!=m0 else float('inf') # gradient -> apply to original pixel coordinates to find intercepts with bounding box.
  # if m==2*pi/10==0.628318 (original test value), gradient is infinite.

  # m, rO, cO -> rA, cA, rB, cB (intercepts with bounding box)

  # 5. get points of intersection for bounding box and draw line on edge image
  a, b = edge.shape

  rA = (rp - m*cp if rp - m*cp < a else a-1) if rp - m*cp >= 0 else 0
  rB = (rp - m*(cp - b) if rp - m*(cp - b) >= 0 else 0) if rp - m*(cp - b) < a else a-1

  if m!=0:
    cA = (cp - rp/m if cp - rp/m < b else b-1) if cp - rp/m >= 0 else 0
    cB = (cp - (rp - a)/m if cp - (rp - a)/m >=0 else 0) if cp - (rp - a)/m < b else b-1
  else:
    cA = 0
    cB = b-1

  rA, rB, cA, cB = tuple(np.array([rA, rB, cA, cB]).astype(int))

  d = int(np.sqrt((rA-rB)**2 + (cA-cB)**2))
  line = (np.linspace(rA,rB,d).astype(int), np.linspace(cA,cB,d).astype(int))

  lines[line] = 255

# plt.imshow(lines+edge.astype(int)*255, cmap='Greys_r', interpolation='nearest')
# plt.imshow(mask, cmap='Greys_r')
# plt.show()

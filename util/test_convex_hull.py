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

img = imread(input_path)

L, n = label(img)

img1 = np.zeros(img.shape)
img1[L==1] = 255
img1 = erode(img1, iterations=20)

edge = img1 - erode(img1)
edge, (r0, c0, r1, c1) = cut_to_black(edge)

# make convex hull of shape
class Hull():
  def __init__(self):
    self.vertices = []

class Vertex():
  def __init__(self, r, c, previous_vertex=None):
    self.r = r
    self.c = c
    self.previous_vertex = previous_vertex

  def __str__(self):
    return '{}, {} -> |{}, {}|'.format(self.previous_vertex.r if self.previous_vertex is not None else 'None', self.previous_vertex.c if self.previous_vertex is not None else 'None', self.r, self.c)

  def test_shape(self, img):
    # 1. draw line between self and previous vertex
    d = int(np.sqrt((self.r - self.previous_vertex.r)**2 + (self.c - self.previous_vertex.c)**2)) + 1
    line = (np.linspace(self.r,self.previous_vertex.r,d).astype(int), np.linspace(self.c,self.previous_vertex.c,d).astype(int))

    # 2. test img is on between points
    test = img[line].sum() == d

    # 3. return true if all on
    return test, img[line]

# 1. initialise with corners of rectangle in a counter-clockwise order, make loop
a, b = edge.shape
hull = Hull()
previous_vertex = None
first_vertex = None
point_list = [(0,0),(0,b-1),(a-1,b-1),(a-1,0)]
for i,(r,c) in enumerate(point_list):
  vertex = Vertex(r,c,previous_vertex)
  if i==0:
    first_vertex = vertex
  elif i==len(point_list)-1:
    first_vertex.previous_vertex = vertex

  hull.vertices.append(vertex)
  previous_vertex = vertex

# 2. test each line for "on"
for vertex in hull.vertices:
  vertex.test_shape(edge)

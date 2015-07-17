import os
import math
import numpy as np
import re
from scipy.misc import imread
from scipy.ndimage.measurements import label
import matplotlib.pyplot as plt
from scipy.ndimage.morphology import binary_erosion as erode
from scipy.ndimage.morphology import binary_dilation as dilate
from scipy.ndimage.measurements import center_of_mass as com
from scipy.ndimage.interpolation import map_coordinates
from scipy.spatial import ConvexHull

input_dir = '/Volumes/transport/data/puzzle/050714/img/region'
track_file = '/Volumes/transport/data/puzzle/050714/track/050714_s13_type-regions_0UY78ED4.csv'
temp = r'050714_s13_ch-regionimg_t(?P<t>[0-9]+)\.tiff'

with open(track_file, 'w+') as track:
  track.write('expt,series,channel,t,region,r,c\n')
  # for each image in the input, segment into regions and translate into marker points on the perimeter
  for image_file_name in [f for f in os.listdir(input_dir) if '.DS' not in f]:
    m = re.match(temp, image_file_name)
    t = int(m.group('t'))
    print(t)
    img = imread(os.path.join(input_dir, image_file_name))

    img = img[:,:,0]
    img[img<img.max()] = 0
    img[img>0] = 1
    img, n = label(img)

    if len(np.unique(img))>5:
      img[img==3] = 0
      img[img==4] = 0
      img[img==5] = 3
      img[img==6] = 4

    # get perimeter
    for u in np.unique(img):
      if u>0:
        mask = np.zeros(img.shape)
        mask[img!=u] = 0
        mask[img==u] = 1
        edge = mask - erode(mask)

        # recompose into single blob
        # blank = np.zeros(edge.shape)
        #
        # for r in range(edge.shape[0]):
        #   for c in range(edge.shape[1]):
        #     up = edge[:r,c]
        #     down = edge[r:,c]
        #     left = edge[r,:c]
        #     right = edge[r,c:]
        #     print(r, c, edge[r,c]==1, np.sum(up==1), np.sum(down==1), np.sum(left==1), np.sum(right==1))
        #     # print(up.shape, down.shape, left.shape, right.shape)
        #     if up.sum()>0 and down.sum()>0 and left.sum()>0 and right.sum()>0:
        #       blank[r,c] = 255
        #
        # plt.imshow(blank, cmap='Greys_r')
        # plt.show()

        # after that is shown, print out points to a file

        w = np.where(edge==1)
        points = [(r,c) for r,c in zip(w[0], w[1])]
        for point in points:
          track.write('{},{},{},{},{},{},{}\n'.format('050714','13','-zbf',t,5-u,point[0],point[1]))

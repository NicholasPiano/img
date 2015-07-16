# woot.apps.img.models

# django
from django.db import models

# local
from apps.expt.models import Experiment, Series
from apps.expt.util import generate_id_token
from apps.img import algorithms

# util
import os
import re
from scipy.misc import imread, imsave, toimage
from skimage import exposure
import numpy as np

### Models
# http://stackoverflow.com/questions/19695249/load-just-part-of-an-image-in-python
class Composite(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='composites')
  series = models.ForeignKey(Series, related_name='composites')

  # properties
  id_token = models.CharField(max_length=8)

  # methods
  def __str__(self):
    return '{}, {} > {}'.format(self.experiment.name, self.series.name, self.id_token)

  def save_data_file(self):
    # save data on all cell instances
    pass

class Template(models.Model):
  # connections
  composite = models.ForeignKey(Composite, related_name='templates')

  # properties
  name = models.CharField(max_length=255)
  rx = models.CharField(max_length=255)
  rv = models.CharField(max_length=255)

  # methods
  def __str__(self):
    return '{}: {}'.format(self.name, self.rx)

  def match(self, string):
    return re.match(self.rx, string)

  def dict(self, string):
    return self.match(string).groupdict()

### GONS
class Channel(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='channels')
  series = models.ForeignKey(Series, related_name='channels')
  composite = models.ForeignKey(Composite, related_name='channels')

  # properties
  name = models.CharField(max_length=255)

  # methods
  def __str__(self):
    return '{} > {}'.format(self.composite.id_token, self.name)

  def segment(self, marker_channel, pipeline_name):
    pass

  def segment_regions(self, region_marker_channel, pipeline_name):
    pass

class Gon(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='gons')
  series = models.ForeignKey(Series, related_name='gons')
  composite = models.ForeignKey(Composite, related_name='gons', null=True)
  template = models.ForeignKey(Template, related_name='gons', null=True)
  channel = models.ForeignKey(Channel, related_name='gons')
  gon = models.ForeignKey('self', related_name='gons', null=True)

  # properties
  id_token = models.CharField(max_length=8, default='')

  # 1. origin
  r = models.IntegerField(default=0)
  c = models.IntegerField(default=0)
  z = models.IntegerField(default=0)
  t = models.IntegerField(default=-1)

  # 2. extent
  rs = models.IntegerField(default=-1)
  cs = models.IntegerField(default=-1)
  zs = models.IntegerField(default=1)

  # 3. data
  array = None

  # methods
  def set_origin(self, r, c, z, t):
    self.r = r
    self.c = c
    self.z = z
    self.t = t
    self.save()

  def set_extent(self, rs, cs, zs):
    self.rs = rs
    self.cs = cs
    self.zs = zs
    self.save()

  def shape(self):
    if self.zs==1:
      return (self.rs, self.cs)
    else:
      return (self.rs, self.cs, self.zs)

  def t_str(self):
    return str('0'*(len(str(self.series.ts)) - len(str(self.t))) + str(self.t))

  def z_str(self, z=None):
    return str('0'*(len(str(self.series.zs)) - len(str(self.z if z is None else z))) + str(self.z if z is None else z))

  def load(self):
    self.array = []
    for path in self.paths.order_by('z'):
      array = imread(path.url)
      self.array.append(array)
    self.array = np.dstack(self.array).squeeze() # remove unnecessary dimensions
    return self.array

  def save_array(self, root, template):
    # 1. iterate through planes in bulk
    # 2. for each plane, save plane based on root, template
    # 3. create path with url and add to gon

    if not os.path.exists(root):
      os.makedirs(root)

    file_name = template.rv.format(self.experiment.name, self.series.name, self.channel.name, self.t, '{}')
    url = os.path.join(root, file_name)

    if len(self.array.shape)==2:
      imsave(url.format(self.z), self.array)
      self.paths.create(composite=self.composite if self.composite is not None else self.gon.composite, channel=self.channel, template=template, url=url.format(self.z), file_name=file_name.format(self.z), t=self.t, z=self.z)

    else:
      for z in range(self.array.shape[2]):
        plane = self.array[:,:,z].copy()

        imsave(url.format(z+self.z), plane) # z level is offset by that of original gon.
        self.paths.create(composite=self.composite, channel=self.channel, template=template, url=url.format(self.z), file_name=file_name.format(self.z), t=self.t, z=z+self.z)

        # create gons
        gon = self.gons.create(experiment=self.composite.experiment, series=self.composite.series, channel=self.channel, template=template)
        gon.set_origin(self.r, self.c, z, self.t)
        gon.set_extent(self.rs, self.cs, 1)

        gon.array = plane.copy().squeeze()

        gon.save_array(self.experiment.composite_path, template)
        gon.save()

### GON STRUCTURE AND MODIFICATION ###
class Path(models.Model):
  # connections
  composite = models.ForeignKey(Composite, related_name='paths')
  gon = models.ForeignKey(Gon, related_name='paths')
  channel = models.ForeignKey(Channel, related_name='paths')
  template = models.ForeignKey(Template, related_name='paths')

  # properties
  url = models.CharField(max_length=255)
  file_name = models.CharField(max_length=255)
  t = models.IntegerField(default=0)
  z = models.IntegerField(default=0)

  # methods
  def __str__(self):
    return '{}: {}'.format(self.composite.id_token, self.file_name)

  def load(self):
    return imread(self.url)

class Mod(models.Model):
  # connections
  composite = models.ForeignKey(Composite, related_name='mods')

  # properties
  id_token = models.CharField(max_length=8)
  algorithm = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)

  # methods
  def run(self):
    ''' Runs associated algorithm to produce a new channel. '''
    algorithm = getattr(algorithms, self.algorithm)
    algorithm(self.composite, self.id_token, self.algorithm)

### MASKS
class MaskChannel(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='mask_channels')
  series = models.ForeignKey(Series, related_name='mask_channels')
  composite = models.ForeignKey(Composite, related_name='mask_channels')

  # properties
  name = models.CharField(max_length=255)

  # methods
  def __str__(self):
    return 'mask {} > {}'.format(self.composite.id_token, self.name)

class Mask(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='masks')
  series = models.ForeignKey(Series, related_name='masks')
  composite = models.ForeignKey(Composite, related_name='masks', null=True)
  channel = models.ForeignKey(MaskChannel, related_name='masks')
  template = models.ForeignKey(Template, related_name='masks', null=True)

  # properties
  id_token = models.CharField(max_length=8, default='')
  url = models.CharField(max_length=255)
  file_name = models.CharField(max_length=255)

  # 1. origin
  r = models.IntegerField(default=0)
  c = models.IntegerField(default=0)
  z = models.IntegerField(default=0)
  t = models.IntegerField(default=-1)

  # 2. extent
  rs = models.IntegerField(default=-1)
  cs = models.IntegerField(default=-1)
  zs = models.IntegerField(default=1)

  # 3. data
  array = None

  # methods
  def set_origin(self, r, c, z, t):
    self.r = r
    self.c = c
    self.z = z
    self.t = t
    self.save()

  def set_extent(self, rs, cs, zs):
    self.rs = rs
    self.cs = cs
    self.zs = zs
    self.save()

  def shape(self):
    if self.zs==1:
      return (self.rs, self.cs)
    else:
      return (self.rs, self.cs, self.zs)

  def t_str(self):
    return str('0'*(len(str(self.series.ts)) - len(str(self.t))) + str(self.t))

  def z_str(self, z=None):
    return str('0'*(len(str(self.series.zs)) - len(str(self.z if z is None else z))) + str(self.z if z is None else z))

  def load(self):
    array = imread(self.url)
    self.array = exposure.rescale_intensity(array * 1.0) * (len(np.unique(array)) - 1).astype(int) # rescale to contain integer grayscale id's.
    return self.array

  def save_array(self, root, template):
    if not os.path.exists(root):
      os.makedirs(root)

    self.file_name = template.rv.format(self.experiment.name, self.series.name, self.channel.name, self.t, '{}')
    self.url = os.path.join(root, file_name).format(self.z)

    imsave(self.url, self.array)
    self.save()

### DATA
class DataFile(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='data_files')
  series = models.ForeignKey(Series, related_name='data_files')
  composite = models.ForeignKey(Composite, related_name='data_files')
  template = models.ForeignKey(Template, related_name='data_files')

  # properties
  url = models.CharField(max_length=255)
  file_name = models.CharField(max_length=255)

  data = []

  # methods
  def load(self):
    pass
    # parse cell profiler results spreadsheet into array that can be used to make cell instances
    # 1. generate dictionary keys from title line
    # 2. return array of dictionaries

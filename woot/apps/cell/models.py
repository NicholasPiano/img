# woot.apps.cell.models

# django
from django.db import models

# local
from apps.expt.models import Experiment, Series
from apps.img.models import Composite, Channel, Gon, Mask
from apps.img.util import *

# util
import numpy as np
from scipy.ndimage.morphology import binary_dilation as dilate
from scipy.signal import find_peaks_cwt as find_peaks
import matplotlib.pyplot as plt

### Models
### MARKERS
class Track(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='tracks')
  series = models.ForeignKey(Series, related_name='tracks')
  composite = models.ForeignKey(Composite, related_name='tracks')
  channel = models.ForeignKey(Channel, related_name='tracks')

  # properties
  track_id = models.IntegerField(default=0)

class TrackInstance(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='track_instances')
  series = models.ForeignKey(Series, related_name='track_instances')
  composite = models.ForeignKey(Composite, related_name='track_instances')
  track = models.ForeignKey(Track, related_name='track_instances')

  # properties
  t = models.IntegerField(default=0)

  # methods
  def primary(self, marker_channel=None): # produce primary image of particular channel
    pass
    # 1. draw white square on black background

class Marker(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='markers')
  series = models.ForeignKey(Series, related_name='markers')
  composite = models.ForeignKey(Composite, related_name='markers')
  channel = models.ForeignKey(Channel, related_name='markers')
  gon = models.ForeignKey(Gon, related_name='markers')
  track = models.ForeignKey(Track, related_name='markers')
  track_instance = models.ForeignKey(TrackInstance, related_name='markers')

  # properties
  r = models.IntegerField(default=0)
  c = models.IntegerField(default=0)
  z = models.IntegerField(default=0)

### REGIONS
class RegionTrack(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='region_tracks')
  series = models.ForeignKey(Series, related_name='region_tracks')
  composite = models.ForeignKey(Composite, related_name='region_tracks')
  channel = models.ForeignKey(Channel, related_name='region_tracks')

class RegionTrackInstance(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='region_track_instances')
  series = models.ForeignKey(Series, related_name='region_track_instances')
  composite = models.ForeignKey(Composite, related_name='region_track_instances')

  # properties
  t = models.IntegerField(default=0)

  # methods
  def primary(self, region_marker_channel=None): # make image using markers as waypoints for outer shell and fill with white
    pass
    # 1. draw lines between each marker in sequence to form a loop
    # 2. fill interior with white

class RegionMarker(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='region_markers')
  series = models.ForeignKey(Series, related_name='region_markers')
  composite = models.ForeignKey(Composite, related_name='region_markers')
  channel = models.ForeignKey(Channel, related_name='region_markers')
  gon = models.ForeignKey(Gon, related_name='region_markers')
  region_track = models.ForeignKey(Track, related_name='region_markers')
  region_track_instance = models.ForeignKey(TrackInstance, related_name='region_markers')

  # properties
  r = models.IntegerField(default=0)
  c = models.IntegerField(default=0)

### REALITY
## REGION
class Region(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='regions')
  series = models.ForeignKey(Series, related_name='regions')
  region_track = models.OneToOneField(RegionTrack, related_name='regions')

class RegionInstance(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='region_instances')
  series = models.ForeignKey(Series, related_name='region_instances')
  region = models.ForeignKey(Region, related_name='instances')

class RegionMask(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='region_masks')
  series = models.ForeignKey(Series, related_name='region_masks')
  region = models.ForeignKey(Region, related_name='masks')
  region_instance = models.ForeignKey(RegionInstance, related_name='masks')
  mask = models.ForeignKey(Mask, related_name='region_masks')

  # properties
  gray_value_id = models.IntegerField(default=0)
  area = models.IntegerField(default=0)

  # methods
  def load(self):
    return self.mask.load()

## CELL
class Cell(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='cells')
  series = models.ForeignKey(Series, related_name='cells')
  track = models.OneToOneField(Track, related_name='cell')

  # methods
  def calculate_velocities(self):
    previous_cell_instance = None
    for cell_instance in self.cell_instances.order_by('t'):
      if previous_cell_instance is None:
        cell_instance.vr = 0
        cell_instance.vc = 0
        cell_instance.vz = 0
      else:
        cell_instance.vr = cell_instance.r - previous_cell_instance.r
        cell_instance.vc = cell_instance.c - previous_cell_instance.c
        cell_instance.vz = cell_instance.z - previous_cell_instance.z

      cell_instance.save()
      previous_cell_instance = cell_instance

class CellInstance(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='cell_instances')
  series = models.ForeignKey(Series, related_name='cell_instances')
  cell = models.ForeignKey(Cell, related_name='instances')
  region = models.ForeignKey(Region, related_name='cell_instances', null=True)
  region_instance = models.ForeignKey(RegionInstance, related_name='cell_instances', null=True)
  track_instance = models.OneToOneField(TrackInstance, related_name='cell_instance')

  # properties
  r = models.IntegerField(default=0)
  c = models.IntegerField(default=0)
  z = models.IntegerField(default=0)
  t = models.IntegerField(default=0)

  vr = models.IntegerField(default=0)
  vc = models.IntegerField(default=0)
  vz = models.IntegerField(default=0)

  # 4. cell profiler
  AreaShape_Area = models.IntegerField(default=0)
  AreaShape_Compactness = models.FloatField(default=0.0)
  AreaShape_Eccentricity = models.FloatField(default=0.0)
  AreaShape_EulerNumber = models.FloatField(default=0.0)
  AreaShape_Extent = models.FloatField(default=0.0)
  AreaShape_FormFactor = models.FloatField(default=0.0)
  AreaShape_MajorAxisLength = models.FloatField(default=0.0)
  AreaShape_MaximumRadius = models.FloatField(default=0.0)
  AreaShape_MeanRadius = models.FloatField(default=0.0)
  AreaShape_MedianRadius = models.FloatField(default=0.0)
  AreaShape_MinorAxisLength = models.FloatField(default=0.0)
  AreaShape_Orientation = models.FloatField(default=0.0)
  AreaShape_Perimeter = models.FloatField(default=0.0)
  AreaShape_Solidity = models.FloatField(default=0.0)
  Location_Center_X = models.FloatField(default=0.0)
  Location_Center_Y = models.FloatField(default=0.0)

  # methods
  def R(self):
    return self.r*self.experiment.rmop

  def C(self):
    return self.c*self.experiment.cmop

  def Z(self):
    return self.z*self.experiment.zmop

  def T(self):
    return self.t*self.experiment.tpf

  def V(self):
    return np.sqrt(self.VR()**2 + self.VC()**2)

  def VR(self):
    return self.vr*self.experiment.rmop / self.experiment.tpf

  def VC(self):
    return self.vc*self.experiment.cmop / self.experiment.tpf

  def VZ(self):
    return self.vz*self.experiment.zmop / self.experiment.tpf

  def A(self):
    return self.AreaShape_Area*self.experiment.rmop*self.experiment.cmop

  def raw_line(self):
    return '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{} \n'.format(self.experiment.name,
                                                                                                  self.series.name,
                                                                                                  self.cell.pk,
                                                                                                  self.r,
                                                                                                  self.c,
                                                                                                  self.z,
                                                                                                  self.t,
                                                                                                  self.vr,
                                                                                                  self.vc,
                                                                                                  self.vz,
                                                                                                  self.region.index,
                                                                                                  self.AreaShape_Area,
                                                                                                  self.AreaShape_Compactness,
                                                                                                  self.AreaShape_Eccentricity,
                                                                                                  self.AreaShape_EulerNumber,
                                                                                                  self.AreaShape_Extent,
                                                                                                  self.AreaShape_FormFactor,
                                                                                                  self.AreaShape_MajorAxisLength,
                                                                                                  self.AreaShape_MaximumRadius,
                                                                                                  self.AreaShape_MeanRadius,
                                                                                                  self.AreaShape_MedianRadius,
                                                                                                  self.AreaShape_MinorAxisLength,
                                                                                                  self.AreaShape_Orientation,
                                                                                                  self.AreaShape_Perimeter,
                                                                                                  self.AreaShape_Solidity)
  def line(self):
    return '{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(self.experiment.name,
                                                                                                    self.series.name,
                                                                                                    self.cell.pk,
                                                                                                    self.R(),
                                                                                                    self.C(),
                                                                                                    self.Z(),
                                                                                                    self.t,
                                                                                                    self.T(),
                                                                                                    self.VR(),
                                                                                                    self.VC(),
                                                                                                    self.VZ(),
                                                                                                    self.region.index,
                                                                                                    self.A(),
                                                                                                    self.AreaShape_Compactness,
                                                                                                    self.AreaShape_Eccentricity,
                                                                                                    self.AreaShape_EulerNumber,
                                                                                                    self.AreaShape_Extent,
                                                                                                    self.AreaShape_FormFactor,
                                                                                                    self.AreaShape_MajorAxisLength,
                                                                                                    self.AreaShape_MaximumRadius,
                                                                                                    self.AreaShape_MeanRadius,
                                                                                                    self.AreaShape_MedianRadius,
                                                                                                    self.AreaShape_MinorAxisLength,
                                                                                                    self.AreaShape_Orientation,
                                                                                                    self.AreaShape_Perimeter,
                                                                                                    self.AreaShape_Solidity)

class CellMask(models.Model):
  # connections
  experiment = models.ForeignKey(Experiment, related_name='cell_masks')
  series = models.ForeignKey(Series, related_name='cell_masks')
  cell = models.ForeignKey(Cell, related_name='masks')
  cell_instance = models.ForeignKey(CellInstance, related_name='masks')
  mask = models.ForeignKey(Mask, related_name='cell_masks')
  marker = models.OneToOneField(Marker, related_name='cell_mask')

  # properties
  gray_value_id = models.IntegerField(default=0)
  area = models.IntegerField(default=0)

  # methods
  def load(self):
    return self.mask.load()

# expt.command: step03_tracking

# django
from django.core.management.base import BaseCommand, CommandError

# local
from apps.img.models import Composite
from apps.expt.util import *

# util
import os
from optparse import make_option
import numpy as np

### Command
class Command(BaseCommand):
  option_list = BaseCommand.option_list + (

    make_option('--expt', # option that will appear in cmd
      action='store', # no idea
      dest='expt', # refer to this in options variable
      default='050714-test', # some default
      help='Name of the experiment to import' # who cares
    ),

    make_option('--series', # option that will appear in cmd
      action='store', # no idea
      dest='series', # refer to this in options variable
      default='13', # some default
      help='Name of the series' # who cares
    ),

  )

  args = ''
  help = ''

  def handle(self, *args, **options):
    '''
    1. What does this script do?
    > Make images that can be recognized by CellProfiler by multiplying smoothed GFP with the flattened Brightfield

    2. What data structures are input?
    > Channel

    3. What data structures are output?
    > Channel

    4. Is this stage repeated/one-time?
    > One-time

    Steps:

    1. Select composite
    2. Call pmod mod on composite
    3. Run

    '''

    # 1. select composite
    composite = Composite.objects.get(experiment__name=options['expt'], series__name=options['series'])

    # 2. check track directory and make tracks
    file_list = [file_name for file_name in os.listdir(composite.experiment.track_path) if '.csv' in file_name]

    for file_name in file_list:
      # get template
      template = composite.experiment.templates.get(name='track')

      # check series name and load
      dict = template.dict(file_name)
      if dict['series']==composite.series.name:
        with open(os.path.join(composite.experiment.track_path, file_name), 'r') as track_file:

          tracks = {} # stores list of tracks that can then be put into the database

          lines = track_file.readlines()
          for i, line in enumerate(lines): # omit title line and final blank line
            print('step03 | reading tracks and markers from {} for {}.{}: ({}/{})'.format(file_name, composite.experiment.name, composite.series.name, i+1, len(lines)))
            line = line.split('\t')

            # details
            track_id = int(float(line[0]))
            r = int(float(line[3]))
            c = int(float(line[2]))
            t = int(float(line[1])) - 1

            if track_id in tracks:
              tracks[track_id].append((r,c,t))
            else:
              tracks[track_id] = [(r,c,t)]

          for track_id, markers in tracks.items():
            track_index = composite.series.tracks.filter(track_id=track_id).count()
            track, track_created = composite.series.tracks.get_or_create(experiment=composite.experiment, series=composite.series, track_id=track_id, index=track_index)

            if track_created:
              for marker in markers:
                track.markers.create(experiment=composite.experiment, series=composite.series, r=marker[0], c=marker[1], t=marker[2])

    # 3. determine region of each marker
    for t in range(composite.series.ts):
      # load region image
      region_gon = composite.gons.get(channel__name='-regions', t=t)
      regions = region_gon.load()
      region_indexes = list(np.unique(regions))

      # get markers
      for marker in composite.series.markers.filter(t=t):
        r, c = marker.r, marker.c

        region_index = region_indexes.index(regions[r,c])
        true_region_index = composite.series.vertical_sort_for_region_index(region_index)

        # get region object
        region = composite.series.regions.get(index=true_region_index)
        marker.region = region
        marker.save()

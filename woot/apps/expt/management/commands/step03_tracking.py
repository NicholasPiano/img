# expt.command: step03_tracking

# django
from django.core.management.base import BaseCommand, CommandError

# local
from apps.img.models import Composite
from apps.expt.util import *
from apps.expt.data import *

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

    # select composite
    composite = Composite.objects.get(experiment__name=options['expt'], series__name=options['series'])

    # add all track files to composite
    data_file_list = [f for f in os.listdir(composite.experiment.track_path) if (os.path.splitext(f)[1] in allowed_data_extensions and composite.experiment.path_matches_series(f, composite.series.name))]

    for df_name in data_file_list:
      data_file, data_file_created, status = composite.get_or_create_data_file(df_name)

    ### REGIONS
    # 1. check for existing track files


    ### MARKERS

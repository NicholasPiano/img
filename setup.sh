#!/bin/sh

sh rmm.sh;
sh mm.sh;
sh db.sh;
python manage.py syncdb;
python manage.py step01_input;
python manage.py step03_tracking;

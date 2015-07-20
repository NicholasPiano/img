#!/bin/sh

sh rmm.sh;
sh mm.sh;
sh db.sh;
python manage.py syncdb;
python manage.py step01_input --expt=050714;
python manage.py step02_zmod --expt=050714;
python manage.py step03_tracking --expt=050714;

#!/bin/sh

pg_dump -U img img_db -f db/img_db.sql
sh db.sh
psql -U img -d img_db -f db/img_db.sql

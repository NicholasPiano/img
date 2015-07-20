#!/bin/sh

sh db.sh
psql -U img -d img_db -f db/img_db.sql

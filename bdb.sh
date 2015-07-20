#!/bin/sh

pg_dump -U img img_db -f db/img_db_full.sql

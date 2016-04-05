#!/usr/bin/env bash

learn discrat \
    --xy-data s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459878060/filter/data_xy.csv \
    --x-data s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459878060/filter/data_x_filtered.csv \
    --dfunct s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459878060/lda/DFUNCT.csv \
    --idf s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459878060/data_idf.csv \
    --varset 18 \
    --output s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459878060/discrat

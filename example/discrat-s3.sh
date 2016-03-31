#!/usr/bin/env bash

learn discrat \
    --xy-data s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20160322-asd34/filter/data_xy.csv \
    --x-data s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20160322-asd34/filter/data_x_filtered.csv \
    --dfunct s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20160322-asd34/lda/DFUNCT.csv \
    --idf s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20160322-asd34/IDF.csv \
    --varset 18 \
    --output ./example/discrat

#!/usr/bin/env bash

learn lda \
    --xy-data s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459887448/filter/data_xy.csv \
    --config s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459887448/varsel/XVARSELV.csv \
    --output s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459887448/lda

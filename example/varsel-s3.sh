#!/usr/bin/env bash

learn varsel \
    --xy-data s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459798999/filter/data_xy.csv \
    --config s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459798999/filter/vsel_xy_config.csv \
    --output s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459798999/varsel

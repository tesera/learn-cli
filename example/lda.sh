#!/usr/bin/env bash

learn lda \
    --xy-data ./example/input/data_xy.csv \
    --config ./example/output/vsel_x.csv \
    --output ./example/output \
    --yvar VAR47

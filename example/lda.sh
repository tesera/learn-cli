#!/usr/bin/env bash

learn lda \
    --xy-data ./example/data_xy.csv \
    --config ./example/varsel/XVARSELV.csv \
    --output ./example/lda \
    --yvar CLPRDP

#!/usr/bin/env bash

learn lda \
    --xy-data ./example/varsel/ANALYSIS.csv \
    --config ./example/varsel/XVARSELV1.csv \
    --output ./example/lda \
    --yvar CLPRDP

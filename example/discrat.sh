#!/usr/bin/env bash

learn discrat \
    --xy-data ./example/lda/ANALYSIS.csv \
    --x-data ./example/lda/ANALYSIS.csv \
    --dfunct ./example/lda/DFUNCT.csv \
    --idf ./example/IDF.csv \
    --varset 18 \
    --output ./example/discrat

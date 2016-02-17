#!/usr/bin/env bash

varselect \
  /opt/varselect/example/ANALYSIS.csv \
  /opt/varselect/example/XVARSELV1.csv \
  /opt/varselect/example/output \
  --classVariableName CLASS5 \
  --excludeRowValue -1 \
  --excludeRowVarName SORTGRP \
  --minNvar 1 \
  --maxNvar 20 \
  --nSolutions 20 \
  --criteria xi2

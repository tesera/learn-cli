#!/usr/bin/env bash

learn varsel \
  /opt/learn/example/ANALYSIS.csv \
  /opt/learn/example/XVARSELV1.csv \
  /opt/learn/example/output \
  --classVariableName CLASS5 \
  --excludeRowValue -1 \
  --excludeRowVarName SORTGRP \
  --minNvar 1 \
  --maxNvar 20 \
  --nSolutions 20 \
  --criteria xi2

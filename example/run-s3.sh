#!/usr/bin/env bash

learn varsel \
  s3://tesera.svc.learn/uploads/example/ANALYSIS.csv \
  s3://tesera.svc.learn/uploads/example/XVARSELV1.csv \
  s3://tesera.svc.learn/uploads/example/output/1 \
  --classVariableName CLASS5 \
  --excludeRowValue -1 \
  --excludeRowVarName SORTGRP \
  --minNvar 1 \
  --maxNvar 20 \
  --nSolutions 20 \
  --criteria xi2

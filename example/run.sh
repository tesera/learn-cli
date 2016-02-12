#!/usr/bin/env bash

varselect \
  s3://tesera.svc.variable-selection/uploads/22a7f809-b28e-4ff5-bb05-39c126e45605/ANALYSIS.csv \
  s3://tesera.svc.variable-selection/uploads/22a7f809-b28e-4ff5-bb05-39c126e45605/XVARSELV1.csv \
  s3://tesera.svc.variable-selection/uploads/22a7f809-b28e-4ff5-bb05-39c126e45605/output/1 \
  --classVariableName CLASS5 \
  --excludeRowValue -1 \
  --excludeRowVarName SORTGRP \
  --minNvar 1 \
  --maxNvar 20 \
  --nSolutions 20 \
  --criteria xi2

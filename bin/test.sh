#!/bin/bash

echo "Comparing outputs of Rwd to tests/regression/$DATASET."
for i in $(\ls -d $MRATPATH/tests/regression/$DATASET/*); do diff ${i} $MRATPATH/Rwd/; done

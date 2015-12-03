#!/bin/bash
#rm -fr /tmp/$DATASET/* && cp tests/data/$DATASET/* /tmp/$DATASET

#cp /tmp/$DATASET/UCORCOEF.csv /tmp/$DATASET/UNIQUEVAR.csv /tmp/$DATASET/VARRANK.csv /tmp/$DATASET/VARSELECT.csv /tmp/$DATASET/XVARSELV1.csv	/tmp/$DATASET/XVARSELV1_XCOUNT.csv /tmp/$DATASET/XVARSELV.csv tests/regression/$DATASET/

echo "Comparing outputs of Rwd to tests/regression/$DATASET."
for i in $(\ls -d $MRATPATH/tests/regression/$DATASET/*); do diff ${i} /tmp/$DATASET/; done

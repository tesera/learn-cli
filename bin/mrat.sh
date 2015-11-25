#!/bin/bash

if [ "$DATASET" = "" ]
    then
	    echo "DATASET env variable missing. Set one from options in tests/data."
  	else	
		echo "Processing $DATASET."
		R CMD Rserve --RS-conf /tmp/Rserv.conf 
		cd $MRATPATH/bin
		cp $MRATPATH/tests/data/$DATASET/*.csv $MRATPATH/Rwd/
		cp $MRATPATH/tests/data/$DATASET/XIterativeVarSel.R.conf $MRATPATH/etc/
		python test_mrat_variable_selection.py
		echo "Comparing outputs of Rwd to tests/regression/$DATASET."
		for i in $(\ls -d $MRATPATH/tests/regression/$DATASET/*); do diff ${i} $MRATPATH/Rwd/; done
		echo "Successful run should not generate differentials."	
fi

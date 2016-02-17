#!/usr/bin/env bash

install2.r -l $R_LIBS_USER devtools

r ./installGithub2.r tesera/rvarselect -d TRUE -t $GITHUB_TOKEN -r $RVARSELECT_REF

pip install --user "git+https://$GITHUB_TOKEN@github.com/tesera/pyvarselect.git@$PYVARSELECT_REF"

rm -rf /tmp/downloaded_packages/ /tmp/*.rds

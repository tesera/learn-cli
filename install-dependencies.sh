#!/usr/bin/env bash

install2.r -l $R_LIBS_USER devtools

r ./installGithub2.r tesera/rlearn -d TRUE -t $GITHUB_TOKEN -r $RLEARN_REF

pip install --user "git+https://$GITHUB_TOKEN@github.com/tesera/pylearn.git@$PYLEARN_REF"

rm -rf /tmp/downloaded_packages/ /tmp/*.rds

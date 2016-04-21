#!/usr/bin/env bash

echo "github token => $GITHUB_TOKEN"

rm -rf pysite rlibs

mkdir -p {pysite,rlibs}

install2.r -l $R_LIBS_USER devtools

r ./installGithub2.r tesera/rlearn -d TRUE -t $GITHUB_TOKEN -r ${RLEARN_REF-master}

pip install --user "git+https://$GITHUB_TOKEN@github.com/tesera/pylearn.git@${PYLEARN_REF-master}"

pip install --user awscli

rm -rf /tmp/downloaded_packages/ /tmp/*.rds

# if this script is run in interactive mode install the cli too
if [[ $1 == '--dev' ]]
then
    echo 'installing learn-cli...'
    pip install --user -e .
fi

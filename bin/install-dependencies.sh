#!/usr/bin/env bash

rm -rf pysite rlibs

mkdir -p {pysite,rlibs}

install2.r -l $R_LIBS_USER devtools

r ./bin/installGithub2.r tesera/rlearn -d TRUE -r ${RLEARN_REF-v1.0.1}

pip install --user scipy awscli

pip install --user "git+https://github.com/tesera/pylearn.git@${PYLEARN_REF-v1.0.1}"
pip install --user "git+https://github.com/tesera/prelurn.git@${PRELURN_REF-v1.0.0}"

rm -rf /tmp/downloaded_packages/ /tmp/*.rds

# if this script is run in interactive mode install the cli too
if [[ $1 == '--dev' ]]
then
    echo 'installing learn-cli...'
    pip install --user -e .
fi

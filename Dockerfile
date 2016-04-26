
FROM r-base:latest

MAINTAINER Tesera Systems Inc.

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python-dev \
    python-setuptools \
    python-scipy \
    python-pip \
    libssl-dev \
    libxml2 \
    libxml2-dev \
    libcurl4-openssl-dev \
    git \
    bats \
&& rm -rf /var/lib/apt/lists/*

ENV PYLEARN_REF=master
ENV RLEARN_REF=master
ENV WD=/opt/learn
ENV HISTFILE=$WD/.bash_history
ENV PYTHONUSERBASE $WD/pysite
ENV PYTHONPATH=/usr/lib/python2.7/dist-packages:$PYTHONPATH
ENV PY_USER_SCRIPT_DIR $PYTHONUSERBASE/bin
ENV R_LIBS_USER $WD/rlibs
ENV PATH $PATH:$PY_USER_SCRIPT_DIR

WORKDIR $WD

COPY ./bin/installGithub2.r installGithub2.r
COPY ./bin/install-dependencies.sh install-dependencies.sh

RUN bash ./install-dependencies.sh

COPY . $WD

RUN pip install --user .

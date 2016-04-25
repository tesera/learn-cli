
FROM r-base:latest

MAINTAINER Tesera Systems Inc.

ARG GITHUB_TOKEN=$GITHUB_TOKEN
ARG PYLEARN_REF=master
ARG RLEARN_REF=master

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

ENV WD=/opt/learn

RUN bash -c "mkdir -p $WD/{pysite,rlibs}"
WORKDIR $WD

RUN echo "github token => $GITHUB_TOKEN"

ENV HISTFILE=$WD/.bash_history
ENV PYTHONUSERBASE $WD/pysite
ENV PYTHONPATH=/usr/lib/python2.7/dist-packages:$PYTHONPATH
ENV PY_USER_SCRIPT_DIR $PYTHONUSERBASE/bin
ENV R_LIBS_USER $WD/rlibs
ENV PATH $PATH:$PY_USER_SCRIPT_DIR

COPY installGithub2.r installGithub2.r
COPY install-dependencies.sh install-dependencies.sh

RUN bash ./install-dependencies.sh

COPY . $WD

RUN pip install --user .

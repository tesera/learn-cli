
# RUN w/ ARG refs are a seperate layer on purpose to optimize build caching.
# Python user site reference: https://www.python.org/dev/peps/pep-0370

FROM r-base:latest

MAINTAINER Tesera Systems Inc.

ARG GITHUB_TOKEN
ARG PYVARSELECT_REF=master
ARG RVARSELECT_REF=master

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
&& rm -rf /var/lib/apt/lists/*

RUN bash -c "mkdir -p /opt/varselect/{pysite,rlibs}"
COPY . /opt/varselect
WORKDIR /opt/varselect

ENV PYTHONUSERBASE /opt/varselect/pysite
ENV PY_USER_SCRIPT_DIR $PYTHONUSERBASE/bin
ENV R_LIBS_USER /opt/varselect/rlibs
ENV PATH $PATH:$PY_USER_SCRIPT_DIR

RUN install2.r -l $R_LIBS_USER subselect futile.logger devtools roxygen2
RUN r ./installGithub2.r tesera/rvarselect -t $GITHUB_TOKEN -r $RVARSELECT_REF

RUN pip install --user "git+https://$GITHUB_TOKEN@github.com/tesera/pyvarselect.git@$PYVARSELECT_REF#egg=pyvarselect"
RUN pip install --user .

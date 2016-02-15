
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

ENV WD=/opt/varselect
RUN bash -c "mkdir -p $WD/{pysite,rlibs}"
WORKDIR $WD

ENV PYTHONUSERBASE $WD/pysite
ENV PYTHONPATH=/usr/lib/python2.7/dist-packages:$PYTHONPATH
ENV PY_USER_SCRIPT_DIR $PYTHONUSERBASE/bin
ENV R_LIBS_USER $WD/rlibs
ENV PATH $PATH:$PY_USER_SCRIPT_DIR

RUN install2.r -l $R_LIBS_USER devtools

COPY installGithub2.r installGithub2.r
RUN r ./installGithub2.r tesera/rvarselect -t $GITHUB_TOKEN -r $RVARSELECT_REF

RUN pip install --user "git+https://$GITHUB_TOKEN@github.com/tesera/pyvarselect.git@$PYVARSELECT_REF#egg=pyvarselect"

# COPY last since it could invalidate build cache
COPY . $WD

# Install the CLI
RUN pip install --user .

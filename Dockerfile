
FROM r-base:latest

MAINTAINER Tesera Systems Inc.

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python-dev \
        python-setuptools \
        python-scipy \
        python-pip \
        virtualenv \
        libssl-dev \
        libxml2 \
        libxml2-dev \
        libcurl4-openssl-dev \
        git \
&& rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/varselect
COPY . /opt/varselect

WORKDIR /opt/varselect

RUN virtualenv venv && . venv/bin/activate
RUN pip install .

RUN R -e "install.packages(c('subselect', 'futile.logger', 'devtools', 'roxygen2'))"
RUN R -e "library('devtools');"

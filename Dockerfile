FROM r-base:latest
MAINTAINER Tesera Systems Inc.

# Install dependencies
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
        git
&& rm -rf /var/lib/apt/lists/*

RUN pip install rpy2 docopt schema boto3
RUN R -e "install.packages(c('subselect', 'futile.logger', 'devtools', 'roxygen2'))"
RUN R -e "library('devtools');"

RUN mkdir /opt/varselect
COPY . /opt/varselect

RUN chmod +x /opt/varselect/*.py

WORKDIR /opt/varselect

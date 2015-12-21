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

RUN pip install rpy2 docopt schema boto3
RUN R -e "install.packages(c('subselect', 'futile.logger', 'devtools', 'roxygen2'))"
RUN R -e "library('devtools');"

ADD mrat.py /usr/local/bin/mrat
RUN chmod +x /usr/local/bin/mrat

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

RUN pip install rpy2 docopt schema boto3 git+https://boriscosic:614ecbe8af3261c0a37296e76ccb689866d7e5f8@github.com/tesera/libvariableselection.git@master
RUN R -e "install.packages(c('subselect', 'futile.logger', 'devtools', 'roxygen2'))"
RUN R -e "library('devtools');install_github('tesera/dicriminant-analysis-variable-selection', ref = 'master', auth_token='614ecbe8af3261c0a37296e76ccb689866d7e5f8')"

# Setup environment
ENV MRATPATH /opt/MRAT_Refactor
ENV PYTHONPATH $MRATPATH:$MRATPATH/bin:$MRATPATH/lib:$MRATPATH/etc:$MRATPATH/lib/functions:$MRATPATH/etc:$MRATPATH/lib/confighandler:$MRATPATH/share:$MRATPATH/Rwd:$MRATPATH/Rwd/Python:$MRATPATH/Rwd/RScript:$MRATPATH/Rwd/Python/CopyToSitePackages:$MRATPATH/Rwd/Python/Admin:$MRATPATH/Rwd/Python/PyReadError:$MRATPATH/Rwd/Python/DATDICT

RUN mkdir $MRATPATH && mkdir -p /opt/src/libvariableselection && mkdir -p /opt/src/dicriminant-analysis-variable-selection
WORKDIR $MRATPATH

CMD ["/bin/bash", "-c", "python mrat.py"]

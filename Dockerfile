FROM r-base:latest
MAINTAINER Tesera Systems Inc.

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
		r-cran-rserve \
		build-essential \ 
		python-dev \
		python-setuptools \
		python-scipy \
		python-pip \
		libssl-dev \
		libxml2 \
		libxml2-dev \
		libcurl4-openssl-dev

RUN pip install pyRserve
RUN pip install rpy2
RUN R -e 'install.packages(c("subselect", "futile.logger", "devtools", "roxygen2"))'

# Setup environment
ENV MRATPATH /opt/MRAT_Refactor
ENV PYTHONPATH $MRATPATH:$MRATPATH/bin:$MRATPATH/lib:$MRATPATH/etc:$MRATPATH/lib/functions:$MRATPATH/etc:$MRATPATH/lib/confighandler:$MRATPATH/share:$MRATPATH/Rwd:$MRATPATH/Rwd/Python:$MRATPATH/Rwd/RScript:$MRATPATH/Rwd/Python/CopyToSitePackages:$MRATPATH/Rwd/Python/Admin:$MRATPATH/Rwd/Python/PyReadError:$MRATPATH/Rwd/Python/DATDICT

RUN mkdir $MRATPATH
WORKDIR $MRATPATH
CMD ["/bin/bash", "-c", "./bin/mrat.sh"]

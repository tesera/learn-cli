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
		python-pip

RUN pip install pyRserve
RUN R -e 'install.packages(c("subselect"))'

# Setup environment
ENV MRATPATH /opt/MRAT_Refactor
ENV PYTHONPATH $MRATPATH:$MRATPATH/bin:$MRATPATH/lib:$MRATPATH/etc:$MRATPATH/lib/functions:$MRATPATH/etc:$MRATPATH/lib/confighandler:$MRATPATH/share:$MRATPATH/Rwd:$MRATPATH/Rwd/Python:$MRATPATH/Rwd/RScript:$MRATPATH/Rwd/Python/CopyToSitePackages:$MRATPATH/Rwd/Python/Admin:$MRATPATH/Rwd/Python/PyReadError:$MRATPATH/Rwd/Python/DATDICT

RUN mkdir $MRATPATH
ADD etc/Rserv.conf Rserv.conf
CMD ["/bin/bash", "-c", "R CMD Rserve --RS-conf Rserv.conf && cd $MRATPATH/bin && python test_mrat_variable_selection.py"]

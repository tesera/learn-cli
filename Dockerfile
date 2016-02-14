
# RUN w/ ARG refs are a seperate layer on purpose to optimize build caching.

FROM r-base:latest

MAINTAINER Tesera Systems Inc.

ARG GITHUB_TOKEN
ARG GITHUB_REF

# Install Core Dependencies
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

# Copy varselect CLI
RUN bash -c "mkdir -p /opt/varselect/{pysite,rlibs}"
COPY . /opt/varselect
WORKDIR /opt/varselect

# Python user sites: https://www.python.org/dev/peps/pep-0370
ENV PYTHONUSERBASE /opt/varselect/pysite
ENV PATH $PATH:$PYTHONUSERBASE/bin

# Configure R Environment
RUN echo '.libPaths(c("rlibs", "~/userLibrary"))' > .Rprofile \
    && R -e 'install.packages(c("subselect", "futile.logger", "devtools", "roxygen2"))'
RUN R -e 'library("devtools"); install_github("tesera/rvarselect", ref=Sys.getenv("GITHUB_REF", "master"), auth_token=Sys.getenv("GITHUB_TOKEN"))'

# Configure Python Environment
RUN pip install --user .
RUN python -c 'import pip, os; pip.main(["install", "git+https://" + os.getenv("GITHUB_TOKEN") + "@github.com/tesera/pyvarselect.git@" + os.getenv("GITHUB_REF", "master")])'

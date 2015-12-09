FROM r-base:latest
MAINTAINER Tesera Systems Inc.

# Need this for docker
EXPOSE 8000

ENTRYPOINT [ "ls" ]

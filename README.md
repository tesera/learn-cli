# Variable Selection CLI

A variable selection client writen in Python and R. The CLI leverages [pyvarselect](https://github.com/tesera/pyvarselect) and [rvarslect](https://github.com/tesera/rvarselect) libraries. We use rpy2 as a proxy between Python and R.

###Dependencies

* Python 2.7
* R
* pip
* [Github Persona Access Token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
* littler (optional for local)
* virtualenv (recommended for local)
* Docker (optional)
* AWS Access Key (optional)

### Running locally without Docker

#### via git clone

```console
# install dependencies listed above
git clone git@github.com:tesera/varselect-cli.git
cd varselect-cli
bash ./install-dependencies.sh
pip install .
```

#### via git direct install

```console
# update your-github-token -> your github personal access token and github-ref -> i.e. master
bash ./install-dependencies.sh
pip install git+git://<your-github-token>@github.com/tesera/varselect-cli@<github-ref>.git
```

###Running Locally without Docker

Make sure you have installed all the dependencies listed above.

```console
# varselect cli is now in path
$ varselect
Usage:
  varselect LVIFILENAME XVARSELECTFILENAME OUTDIR  \ 
      [--classVariableName=<string>] \
      [--excludeRowValue=<int>]  \
      [--excludeRowVarName=<string>]  \
      [--xVarSelectCriteria=<string>]  \
      [--minNvar=<int>]  \
      [--maxNvar=<int>]  \
      [--nSolutions=<int>]  \
      [--criteria=<int>]  \
      [--tempDir=<string>]
```

###Running with Docker

If you are using docker-machine make sure you have a machine running and that you have evaluated the machine environment.

### Create a virtual machine
```console
docker-machine create --driver virtualbox default
eval "$(docker-machine env default)"
```

### Build the container

```console
git clone git@github.com:tesera/varselect-cli.git
docker build -t="varselect-cli" \
    --build-args GITHUB_TOKEN=<your-github-token> \
    [--build-args PYVARSELECT_REF=<pyvarselect-lib-github-ref> ] \
    [--build-args RVARSELECT_REF=<rvarselect-lib-github-ref> ] \
    varselect-cli
```

### Run the container

### Command

```console
docker run -it -v $PWD/example:/opt/data varselect-cli \
  /opt/data/ANALYSIS.csv \
  /opt/data/XVARSELV1.csv \
  /opt/data \
  --classVariableName CLASS5 \
  --excludeRowValue -1 \
  --excludeRowVarName SORTGRP \
  --minNvar 1 \
  --maxNvar 20 \
  --nSolutions 20 \
  --criteria xi2
```

### Running the Examples

```console
docker run -it varselect-cli bash ./example/run.sh
```

```console
docker run -it \
  -e AWS_ACCESS_KEY_ID=<your-aws-access-key> \
  -e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key> \
  varselect-cli bash ./example/run-s3.sh
```

### Development

```console
cd varselect-cli
docker run -v $PWD:/opt/varselect -it \
  [-e AWS_ACCESS_KEY_ID=<your-aws-access-key>] \
  [-e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>] \
  varselect-cli /bin/bash
```

## Testing
>Tests will be added soon

## Contributing

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [R Style Guide](https://google.github.io/styleguide/Rguide.xml)

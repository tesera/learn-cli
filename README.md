# Variable Selection CLI

The runner consists of two components

- mrat.py: Base varselect tool that logs to command line. Type 'python mrat.py' for usage.
- runner.py: Wrapper around mrat.py that pipes output to Cloudwatch and a log file. Usage, ./runner.py log-id params_for_mrat.py

##Dependencies

* Python 2.7
* pip
* virtualenv (recommended)
* R

##Running Locally

Make sure you have installed all the dependencies listed above.

```shell
$ git clone git@github.com:tesera/varselect-cli.git
$ cd varselect-cli

#optonal: setup isolated env
$ virtualenv venv
$ source venv/bin/activate

# install package and dependencies
$ pip install .

# varselect cli is now in path
$ varselect
Usage:
  varselect LVIFILENAME XVARSELECTFILENAME OUTDIR
  varselect LVIFILENAME XVARSELECTFILENAME OUTDIR  [--classVariableName=<string>]  [--excludeRowValue=<int>]  [--excludeRowVarName=<string>]  [--xVarSelectCriteria=<string>]  [--minNvar=<int>]  [--maxNvar=<int>]  [--nSolutions=<int>]  [--criteria=<int>]  [--tempDir=<string>]
```

##Running the CLI using Docker

If you are using docker-machine make sure you have a machine running and that you have evaluated the machine environment.

```shell
eval "$(docker-machine env default)"
```

### How to build the container

```shell
git clone git@github.com:tesera/varselect-cli.git
docker build -t="varselect-cli" varselect-cli
```

### How to Run the container

In order to run the container you will need an access token for Github API token and access keys for AWS in order to use AWS S3.

### Example

```shell
cd varselect-cli
docker run -it \
  -e GITHUB_TOKEN=<your-github-token> \
  -e AWS_ACCESS_KEY_ID=<your-aws-access-key> \
  -e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key> \
  varselect-cli bash ./example/run.sh
```

### Development

```shell
cd varselect-cli
docker run -v $PWD:/opt/varselect -it \
  -e GITHUB_TOKEN=<your-github-token> \
  -e AWS_ACCESS_KEY_ID=<your-aws-access-key> \
  -e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key> \
  varselect-cli /bin/bash
```

### Production

```shell
cd varselect-cli
docker run \
  -e GITHUB_TOKEN=<your-github-token> \
  -e AWS_ACCESS_KEY_ID=<your-aws-access-key> \
  -e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key> \
  varselect-cli /bin/bash
```

## Testing
To test outputs compare the output directories. In order to create predicatable outputs call to *improve* in rvarselect is set to use the same seed.

## Contributing

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [R Style Guide](https://google.github.io/styleguide/Rguide.xml)

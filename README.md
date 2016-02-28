# Learn CLI

[ ![Codeship Status for tesera/learn-cli](https://codeship.com/projects/f2a31230-b7e8-0133-9192-1269d3e58a72/status?branch=master)](https://codeship.com/projects/134949)

Learn CLI performs variable selection, model development and target dataset processing. The CLI uses [pylearn](https://github.com/tesera/pylearn) and [rlearn](https://github.com/tesera/rlearn) libraries. The CLI is written in Python and uses the rpy2 package to invoke R functions.

The cli is docker ready. You can choose to run the cli locally the old fashion way or through Docker with the Dockerfile included. Running the cli in Docker will simplify the efforts tremendously but Docker is not required.

###Dependencies

* [Github Persona Access Token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
* [AWS Access Key](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html) (optional)

####Without Docker
* [Python 2.7](https://www.python.org/)
* [R](https://www.r-project.org/)
* [pip](https://pypi.python.org/pypi/pip)
* [virtualenv](https://virtualenv.readthedocs.org/en/latest/) (recommended)
* [little r](http://dirk.eddelbuettel.com/code/littler.html)

####With Docker
* [Docker](https://www.docker.com/)
* [Docker Machine](https://docs.docker.com/machine/) (Windows/OSX)

### Running without Docker on OSX (not recommended; use Docker)

In order to run this CLI without Docker you need to install all the lower level dependencies in order to build the higher level dependencies. i.e. gcc, fortran... SciPy is also installed as a system level dependency because of its comples build steps. If you are confident you have all the dependencies installed and configured you can proceed otherwise we recommend the Docker approach.

####Install Python and R Dependencies

```
export GITHUB_TOKEN=<your-github-token>
export PYLEARN_REF=master
export RLEARN_REF=master
export AWS_ACCESS_KEY_ID=<your-access-key>
export AWS_SECRET_ACCESS_KEY=<your-secret-key>
export AWS_REGION=<your-aws-region>

bash ./install-dependencies.sh
```

#### Install via git clone

```console
git clone git@github.com:tesera/learn-cli.git
cd learn-cli
pip install .
```

#### Install via Git direct install

```console
pip install git+git://$GITHUB_TOKEN@github.com/tesera/learn-cli@master.git
```

#### Test the install

```console
$ learn --help
Usage:
    learn <operation> <datafile> <variablesfile> <outputdir> [options]

Arguments:
    <operation> varsel | lda
    <datafile>  Input file, local or S3 in format s3://bucket/path/filename.csv.
    <variablesfile>  File containing variable selections, local or S3 in format s3://bucket/path/filename.csv.
    <outputdir>  Directory to write results out too.

Options:
    --classVariableName=<string>  Class variable name: CLASS5, CLPRDP [default: CLASS5].
    --excludeRowValue=<int>  Variable value to exclude rows from a dataset [default: -1].
    --excludeRowVarName=<string>  Variable name to exclude rows from a dataset [default: SORTGRP].
    --xVarSelectCriteria=<string>  Variable indicator value [default: X].
    --minNvar=<int>  Minimum number of variables to select [default: 1].
    --maxNvar=<int>  Maximum number of variables to select [default: 20].
    --nSolutions=<int>  Number of iterations to be applied [default: 20].
    --criteria=<string>  Set the criteria to be applied for variables selection: ccr12, Wilkes xi2 zeta2 [default: xi2].
    --tempDir=<string>  Use this temp directory instead of generating one.
    --priorDistribution=<string>  TODO: Describe [default: SAMPLE]
    --classNames=<string>  TODO: Describe. [default: CLASS5]
```

### Running with Docker

If you are using docker-machine make sure you have a machine running and that you have evaluated the machine environment.

#### Create a virtual machine with Windows Powershell
```console
docker-machine create --driver virtualbox --virtualbox-host-dns-resolver default
docker-machine env --shell powershell default | Invoke-Expression
```

#### Create a virtual machine with OSX Shell
```console
docker-machine create --driver virtualbox default
eval "$(docker-machine env default)"
```

#### Build the container

```console
git clone git@github.com:tesera/learn-cli.git
cd learn-cli

docker build -t="learn-cli" \
    --build-arg GITHUB_TOKEN=<your-github-token> \
    [--build-arg PYLEARN_REF=<pylearnt-github-ref> ] \
    [--build-arg RLEARN_REF=<rlearn-github-ref> ] \
    learn-cli
```

#### Run the container

#####Basic Command

```console
docker run -it -v $PWD/example:/opt/data learn-cli \
  varsel \
  /opt/data/ANALYSIS.csv \
  /opt/data/XVARSELV1.csv \
  /opt/data/varsel \
  --classVariableName CLASS5 \
  --excludeRowValue -1 \
  --excludeRowVarName SORTGRP \
  --minNvar 1 \
  --maxNvar 20 \
  --nSolutions 20 \
  --criteria xi2
```

##### Running the Examples

```console
docker run -it learn-cli bash ./example/run.sh
```

```console
docker run -it \
  -e AWS_ACCESS_KEY_ID=<your-aws-access-key> \
  -e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key> \
  learn-cli bash ./example/run-s3.sh
```

##### Run in development mode

```console
docker run -v $PWD:/opt/learn -it \
  [-e AWS_ACCESS_KEY_ID=<your-aws-access-key>] \
  [-e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>] \
  learn-cli /bin/bash
```

### Running in AWS ECS

Learn tasks will run by default in the `learn` ECS Cluster. The instances will be placed in the `subnet-tesera-ecs` subnet the `tesera-master` VPC. In order to ssh into your ECS instances you will need to hop from the `master-bastion` server. The `subnet-tesera-ecs` talks out through the NAT Gateway so your instances will not require a public ip.

#####Launching an EC2 Instances to the `learn` ECS Cluster

This step may not be required if there is already an instance running in the `learn` cluster. In cases where you need many instances to run your tasks you can deploy more servers by passing in the instance count as an arg to the `run-instances.sh` script.

```console
# usage: bash ./run-instances.sh [count=1]

# launches 1 instance by default
bash ./run-instances.sh

# launches 5 instances
bash ./run-instances.sh 5
```

#####Registering a Task Definition

In most case you will not need to register a Task Definition since they have been registered already. You will need to register a new task only if you need to change its parameters.

```console
bash ./register-task-definition.sh
```

#####Running a Task

Running the task will run the most recent task definition by default. You can change the args in the `overrides.json` file for your analysis.

```console
# edit overrides.json for your analysis
cat aws/overrides.json
{
  "containerOverrides": [
    {
      "name": "learn",
      "command": [
        "varsel",
        "s3://tesera.svc.learn/uploads/example/ANALYSIS.csv",
        "s3://tesera.svc.learn/uploads/example/XVARSELV1.csv",
        "s3://tesera.svc.learn/uploads/example/varsel",
        "--classVariableName=CLASS5",
        "--excludeRowValue=-1",
        "--excludeRowVarName=SORTGRP",
        "--minNvar=1",
        "--maxNvar=20",
        "--nSolutions=20",
        "--criteria=xi2"
      ]
    }
  ]
}

# run the task with the overides
bash ./run-task.sh

# the results should now be in the specified output path.
aws s3 ls --recursive s3://tesera.svc.learn/uploads/example/varsel
2016-02-18 15:38:36      35048 uploads/example/varsel/ANALYSIS.csv
2016-02-18 15:38:36       5186 uploads/example/varsel/UCORCOEF.csv
2016-02-18 15:38:36        132 uploads/example/varsel/UNIQUEVAR.csv
2016-02-18 15:38:36        281 uploads/example/varsel/VARRANK.csv
2016-02-18 15:38:36      51560 uploads/example/varsel/VARSELECT.csv
2016-02-18 15:38:36       1929 uploads/example/varsel/XVARSELV.csv
2016-02-18 15:38:36        689 uploads/example/varsel/XVARSELV1.csv
2016-02-18 15:38:36          3 uploads/example/varsel/XVARSELV1_XCOUNT.csv

```

### Testing
>Tests will be added soon

### Contributing

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [R Style Guide](https://google.github.io/styleguide/Rguide.xml)

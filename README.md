# Variable Selection CLI

A variable selection client writen in Python and R. The CLI leverages [pyvarselect](https://github.com/tesera/pyvarselect) and [rvarslect](https://github.com/tesera/rvarselect) libraries. We use rpy2 as a proxy between Python and R.

The cli is docker ready. You can choose to run the cli locally the old fashion way or through Docker with the Dockerfile included. Running the cli in Docker will simplify the efforts tremendously but Docker know how is required.

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

### Running without Docker

#### Install via git clone

```console
# install dependencies listed above
git clone git@github.com:tesera/varselect-cli.git
cd varselect-cli
bash ./install-dependencies.sh
pip install .
```

#### Install via git direct install

```console
# update your-github-token -> your github personal access token and github-ref -> i.e. master
bash ./install-dependencies.sh
pip install git+git://<your-github-token>@github.com/tesera/varselect-cli@<github-ref>.git
```

#### Invoke the cli

```console
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

#### Create a virtual machine
```console
docker-machine create --driver virtualbox default
eval "$(docker-machine env default)"
```

#### Build the container

```console
git clone git@github.com:tesera/varselect-cli.git
docker build -t="varselect-cli" \
    --build-arg GITHUB_TOKEN=<your-github-token> \
    [--build-arg PYVARSELECT_REF=<pyvarselect-lib-github-ref> ] \
    [--build-arg RVARSELECT_REF=<rvarselect-lib-github-ref> ] \
    varselect-cli
```

#### Run the container

#####Basic Command

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

##### Running the Examples

```console
docker run -it varselect-cli bash ./example/run.sh
```

```console
docker run -it \
  -e AWS_ACCESS_KEY_ID=<your-aws-access-key> \
  -e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key> \
  varselect-cli bash ./example/run-s3.sh
```

##### Run in development mode

```console
cd varselect-cli
docker run -v $PWD:/opt/varselect -it \
  [-e AWS_ACCESS_KEY_ID=<your-aws-access-key>] \
  [-e AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>] \
  varselect-cli /bin/bash
```

### Running in AWS ECS

Varselect tasks will run by default in the `varselect` ECS Cluster. The instances will be placed in the `subnet-tesera-ecs` subnet the `tesera-master` VPC. In order to ssh into your ECS instances you will need to hop from the `master-bastion` server. The `subnet-tesera-ecs` talks out through the NAT Gateway so your instances will not require a public ip.

#####Launching an EC2 Instances to the varselect ECS Cluster

This step may not be required if there is already an instance running in the varselect cluster. In cases where you need many instances to run your tasks you can deploy more servers by passing in the instance count as an arg to the `launch-instances.sh` script.

```console
# usage: bash ./launch-instances.sh [count=1]

# launches 1 instance by default
bash ./launch-instances.sh

# launches 5 instances
bash ./launch-instances.sh 5
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
      "name": "varselect",
      "command": [
        "s3://tesera.svc.variable-selection/uploads/example/ANALYSIS.csv",
        "s3://tesera.svc.variable-selection/uploads/example/XVARSELV1.csv",
        "s3://tesera.svc.variable-selection/uploads/example/output/1",
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
aws s3 ls --recursive s3://tesera.svc.variable-selection/uploads/example/output/1
2016-02-18 15:38:36      35048 uploads/example/output/1/ANALYSIS.csv
2016-02-18 15:38:36       5186 uploads/example/output/1/UCORCOEF.csv
2016-02-18 15:38:36        132 uploads/example/output/1/UNIQUEVAR.csv
2016-02-18 15:38:36        281 uploads/example/output/1/VARRANK.csv
2016-02-18 15:38:36      51560 uploads/example/output/1/VARSELECT.csv
2016-02-18 15:38:36       1929 uploads/example/output/1/XVARSELV.csv
2016-02-18 15:38:36        689 uploads/example/output/1/XVARSELV1.csv
2016-02-18 15:38:36          3 uploads/example/output/1/XVARSELV1_XCOUNT.csv

```

### Testing
>Tests will be added soon

### Contributing

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [R Style Guide](https://google.github.io/styleguide/Rguide.xml)

# Learn CLI

[ ![Codeship Status for tesera/learn-cli](https://codeship.com/projects/f2a31230-b7e8-0133-9192-1269d3e58a72/status?branch=master)](https://codeship.com/projects/134949)

Learn CLI performs variable selection, model development and target dataset processing. The CLI uses [pylearn](https://github.com/tesera/pylearn) and [rlearn](https://github.com/tesera/rlearn) libraries. The CLI is written in Python and uses the rpy2 package to invoke R functions.

The cli is docker ready. You can choose to run the cli locally the old fashion way or through Docker with the Dockerfile included. Running the cli in Docker will simplify the efforts tremendously but Docker is not required.

```console
$ learn --help
Usage:
    learn varsel (--xy-data <file> --config <file> --yvar <string>) [--iteration <solutions:x-min:x-max> --criteria <string> --output <dir>]
    learn lda (--xy-data <file> --config <file> --yvar <string>) [--iteration <solutions:x-min:x-max> --criteria <string> --output <dir>]
    learn discrat (--xy-data <file> --x-data <file> --dfunct <file> --idf <file> --varset <int>) [--output <dir>]

Options:
    --xy-data <file>  The path to the XY reference CSV file. Can be an S3://... path.
    --x-data <file>  The path to the X filtered data CSV file. Can be an S3://... path.
    --config <file>  Variable selection file. Can be an S3://... path. [default: ./config.csv]
    --yvar <string>  Class variable name: CLASS5, CLPRDP [default: Y].
    --iteration <string>  Iteration specific arguments for variable selection. <solutions:x-min:x-max> [default: 10:1:10]
    --criteria <string>  Set the criteria to be applied for variables selection: ccr12, Wilkes, xi2, zeta2 [default: xi2].
    --dfunct <file>  The path to the lda dfunct file to use for the discriminant rating.
    --idf <file>  The path to the IDF Curves file to use for the discriminant rating.
    --varset <int>  The ID of the varset to use for the discriminant rating.
    --output <dir>  Output folder. [default: ./]
    -h --help  Show help.

Examples:
    learn varsel --xy-data ./folder/xy_reference.csv --config ./folder/xvar_sel.csv --output ./output/varsel --iteration 10:1:10
    learn varsel --xy-data s3://bucket/xy_reference.csv --config s3://bucket/xvar_sel.csv --output s3://bucket/varsel --iteration 10:1:10
    learn lda --xy-data ./folder/xy_reference.csv --config ./folder/xvar_sel.csv --output./output/varsel
    learn lda --xy-data s3://bucket/xy_reference.csv --config s3://bucket/xvar_sel.csv --output s3://bucket/varsel
    learn discrat --xy-data ./folder/xy_reference.csv --x-data ./folder/x_filtered.csv --dfunct ./folder/dfunct.csv --idf ./folder/idf.csv --varset 18 --output ./output/varsel
    learn discrat --xy-data s3://bucket/xy_reference.csv --x-data s3://bucket/x_filtered.csv --dfunct s3://bucket/dfunct.csv --idf s3://bucket/idf.csv --varset 18 --output s3://bucket/varsel
```

###Dependencies

* [Github Persona Access Token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
* [AWS Access Key](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html) (optional)
* `dev.env` file

```console
$ cat dev.env
export GITHUB_TOKEN=<your-github-token>
export PYLEARN_REF=master
export RLEARN_REF=master
export AWS_ACCESS_KEY_ID=<your-access-key>
export AWS_SECRET_ACCESS_KEY=<your-secret-key>
export AWS_REGION=<your-aws-region>
```

####Without Docker
* [Python 2.7](https://www.python.org/)
* [R](https://www.r-project.org/)
* [pip](https://pypi.python.org/pypi/pip)
* [little r](http://dirk.eddelbuettel.com/code/littler.html)

####With Docker
* [Docker](https://www.docker.com/)
* [Docker Machine](https://docs.docker.com/machine/) (Windows/OSX)
* [Docker Compose](https://docs.docker.com/compose/overview/)

### Running with Docker

If you are using docker-machine make sure you have a machine running and that you have evaluated the machine environment.

#### Create a virtual machine with Windows Powershell
```console
$ docker-machine create --driver virtualbox --virtualbox-host-dns-resolver default
$ docker-machine env --shell powershell default | Invoke-Expression
```

#### Create a virtual machine with OSX Shell
```console
$ docker-machine create --driver virtualbox default
$ eval "$(docker-machine env default)"
```

#### Run the container

```console
$ docker-compose run dev
# bash ./install-dependencies.sh --dev
```

### Running without Docker on OSX (not recommended; use Docker)

In order to run this CLI without Docker you need to install all the lower level dependencies in order to build the higher level dependencies. i.e. gcc, fortran... SciPy is also installed as a system level dependency because of its comples build steps. If you are confident you have all the dependencies installed and configured you can proceed otherwise we recommend the Docker approach.


```console
git clone git@github.com:tesera/learn-cli.git
cd learn-cli
source dev.env
bash ./install-dependencies.sh
pip install .
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
cat aws/overrides-varsel.json
{
  "containerOverrides": [
    {
      "name": "learn",
      "command": [
        "varsel",
        "--xy-data=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/filter/data_xy.csv",
        "--config=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/filter/vsel_xy_config.csv",
        "--output=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel"
      ]
    }
  ]
}

cat aws/overrides-lda.json
{
  "containerOverrides": [
    {
      "name": "learn",
      "command": [
        "lda",
        "--xy-data=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/filter/data_xy.csv",
        "--config=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/XVARSELV.csv",
        "--output=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/lda"
      ]
    }
  ]
}

cat aws/overrides-discrat.json
{
  "containerOverrides": [
    {
      "name": "learn",
      "command": [
        "discrat",
        "--xy-data=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/filter/data_xy.csv",
        "--x-data=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/filter/data_x_filtered.csv",
        "--dfunct=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/lda/DFUNCT.csv",
        "--idf=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/data_idf.csv",
        "--varset=18",
        "--output=s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/discrat"
      ]
    }
  ]
}

# run cli via run-task and associated overrides
bash ./run-task.sh (varsel | lda | discrat)

# the results should now be in the specified output path.
aws s3 ls --recursive s3://tesera.svc.learn/organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel
2016-04-01 16:22:42   15256507 organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/ANALYSIS.csv
2016-04-01 16:22:43     267998 organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/UCORCOEF.csv
2016-04-01 16:22:43       1042 organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/UNIQUEVAR.csv
2016-04-01 16:22:43       1892 organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/VARRANK.csv
2016-04-01 16:22:43      21671 organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/VARSELECT.csv
2016-04-01 16:22:43       3767 organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/XVARSELV.csv
2016-04-01 16:22:42      12859 organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/XVARSELV1.csv
2016-04-01 16:22:43          4 organizations/tesera/projects/example/scenarios/20150116-1459525313/varsel/XVARSELV1_XCOUNT.csv

```

### Testing
>Tests will be added soon

### Contributing

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [R Style Guide](https://google.github.io/styleguide/Rguide.xml)

# learn-cli

[ ![Codeship Status for tesera/learn-cli](https://codeship.com/projects/f2a31230-b7e8-0133-9192-1269d3e58a72/status?branch=master)](https://codeship.com/projects/134949)

learn-cli performs variable selection, model development and target dataset processing. It uses [pylearn](https://github.com/tesera/pylearn) and [rlearn](https://github.com/tesera/rlearn) libraries. The cli invokes rlearn function via rpy2.

Although the cli is docker ready you can choose to run the cli locally the old fashion way. Running the cli in Docker will simplify the efforts tremendously but Docker is not required.

### Prerequisites

* R
* Python 2.7
* rlearn `library('devtools'); install_github(repo='tesera/rlearn', dependencies=TRUE, ref='master');`
* AWS Access Keys (optional: for using S3 data location)

### Install

```console
$ pip install git+https://github.com/tesera/learn-cli.git
```

### Usage
```console
$ learn --help
Usage:
    learn varsel (--xy-data <file> --config <file>) [--yvar <string> --iteration <solutions:x-min:x-max> --criteria <string> --output <dir>]
    learn lda (--xy-data <file> --config <file>) [--yvar <string> --output <dir>]
    learn discrat (--xy-data <file> --x-data <file> --dfunct <file> --idf <file> --varset <int>) [--yvar <string> --output <dir>]

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

### Testing

`bats ./tests/intergration`

### Docker

If you are using docker-machine make sure you have a machine running and that you have evaluated the machine environment.

#### Creating a Docker Machine Host VM

#####Windows Powershell
```console
$ docker-machine create --driver virtualbox --virtualbox-host-dns-resolver default
$ docker-machine env --shell powershell default | Invoke-Expression
```

##### OSX
```console
$ docker-machine create --driver virtualbox default
$ eval "$(docker-machine env default)"
```

#### Running the container

```console
$ docker build -t learn .
$ docker run learn /bin/bash
root@1e36bb3275b5:/opt/learn# learn --help
```

#### Development

During development you will want to bring in the codebase with you in the container. You can simply use the Docker Compose command bellow. Once in the container run the `install-dependencies.sh` script passing in the `--dev` flag to make the project editable. This wil install all the Python dependencies in the project root under the `pysite folder and the R dependencies under the rlibs folder. You will only need to run this once unless you dependencies change.

You will need to add a `dev.env` file with at least `PYLEARN_REF` and `RLEARN_REF` variables set to the Github ref/version of the respective libraries. Optionaly you can also add you AWS Access Keys and region in order to use S3 as a data location.

```console
$ cat dev.env
export PYLEARN_REF=master
export RLEARN_REF=master
export AWS_ACCESS_KEY_ID=<your-access-key>
export AWS_SECRET_ACCESS_KEY=<your-secret-key>
export AWS_REGION=<your-aws-region>
```

```console
$ docker-compose run dev
root@1e36bb3275b5:/opt/learn# bash ./install-dependencies --dev
root@1e36bb3275b5:/opt/learn# learn --help
```

#### Testing

`docker-compose run tests`

### Contributing

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [R Style Guide](https://google.github.io/styleguide/Rguide.xml)

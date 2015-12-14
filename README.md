# MRAT Refactor

## Docker Setup

Single line runner in form of bash script or Makefile does not exist for a reason. Help improve the process by working through these steps. 
 
* OSX:
	- Install homebrew: `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
	- Instal virtual box: `brew cask install virtualbox`
	- Install docker: `brew install docker docker-machine` (do not install deprecated boot2docker)	
	- Setup a VM: `docker-machine create -d virtualbox dev`
	- Make sure to follow the instructions to setup environment variables: `docker-machine env dev`. Docker won't work without them.
	- Checkout MRAT_Refactor/slimrat: `git clone git@github.com:tesera/MRAT_Refactor.git && git checkout origin/slimrat -b slimrat`
	- Build docker image: `docker build --rm -t mrat .`


## Working with S3
In order to work with S3 export your S3 keys:
- `export AWS_ACCESS_KEY_ID=YOUR_ID`
- `export AWS_SECRET_ACCESS_KEY=YOUR_KEY`

## Running

Insure docker image is loaded via `docker images`. If *Cannot connect to the Docker daemon. Is the docker daemon running on this host?* error displays this is not an issue with docker or docker-machine. Run `docker-machine env dev` to display and setup environment variables. `dev` is the name of virtual machine that was setup in above step.

To run MRAT copy and paste the following command:

* `docker run -v $PWD:/opt/MRAT_Refactor -it -e DATASET=MONCTON mrat`
	- `-e DATASET=MONCTON` this refers one of the test environments in tests/data. DATASET is the environment variable.
	- bin/mrat.sh is the script that's added to the virtual machine and executes MRAT and tests. 

To run MRAT tests copy and paste the following command:

* `docker run -v $PWD:/opt/MRAT_Refactor -it -e DATASET=MONCTON mrat ./bin/test.sh`

*Note: In order to have tests copy the results of first run to tests/regression/DATASET. Files to copy are noted below. The DATASET must correspond to the runtime folder above that exists in tests/data.*

## Refactoring

Environment variable `DATASET` refers to analysis that is going to run on MRAT. start.sh will copy `tests/data/$DATASET/*.csv` into `Rwd` and `tests/data/$DATASET/XIterativeVarSel.R.conf` into `etc`. Key runtime files are **XVARSELV1.csv** and **ANALYSIS.csv**. **XVARSELV1.csv** is modified by MRAT and cannot be used in subsequent runs. classVariableName in tests/data/$DATASET/XIterativeVarSel.R.conf can be set as either _CLASS5_ or _CLPRDP_

After each run the output in Rwd will be compared following files in tests/regresion/$DATASET and succesfull run should not generate any differentials:
- UCORCOEF.csv
- UNIQUEVAR.csv
- VARRANK.csv 
- VARSELECT.csv 
- XVARSELV.csv
- XVARSELV1_XCOUNT.csv
- XVARSELV1.csv

## Creating an R Library

- Start R console.
- `library('devtools')`
- `library('roxygen2')`
- `setwd('./Rwd')` - this will create the library in Rwd folder
- `create('MyLibrary')

In finder open this folder and inside R create a file, **my_library.R**. Once the function is complete install it with: `install("MyLibrary")
The library can be pushed to github and installed with: `install_github('MyLibrary','github_username')`

To use the library while in development use devtools to install and load it at runtime:
```
install('DiscriminantAnalysisVariableSelection')
library('DiscriminantAnalysisVariableSelection')
```

## Style Guidelines
- [Python](https://www.python.org/dev/peps/pep-0008/)
- [R](https://google.github.io/styleguide/Rguide.xml)

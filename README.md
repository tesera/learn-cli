# MRAT Refactor

## Setup

### Docker

#### OSX:
	- Install homebrew: **ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"**
	- Instal virtual box: **brew install virtualbox**
	- Install docker: **brew install docker** (do not install deprecated boot2docker)	
	- Setup a VM: **docker-machine create -d virtualbox dev**
	- Checkout MRAT_Refactor/slimrat: **git clone git@github.com:tesera/MRAT_Refactor.git && git checkout origin/slimrat -b slimrat**
	- Build docker image: **docker build -t mrat .**
	- Run MRAT: **docker run -v $PWD:/opt/MRAT_Refactor -it mrat**
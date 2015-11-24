# MRAT Refactor

## Setup 
Single line runner in form of bash script or Makefile does not exist for a reason. Help improve the process by working through these steps. 

#### Docker

* OSX:
	- Install homebrew: `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
	- Instal virtual box: `brew cask install virtualbox`
	- Install docker: `brew install docker docker-machine` (do not install deprecated boot2docker)	
	- Setup a VM: `docker-machine create -d virtualbox dev`
	- Make sure to follow the instructions to setup environment variables: `docker-machine env dev`. Docker won't work without them.
	- Checkout MRAT_Refactor/slimrat: `git clone git@github.com:tesera/MRAT_Refactor.git && git checkout origin/slimrat -b slimrat`
	- Build docker image: `docker build -t mrat .`
	- Run MRAT: `docker run -v $PWD:/opt/MRAT_Refactor -it mrat`
	- On new terminal session run: `docker-machine env dev` to configure environment variables

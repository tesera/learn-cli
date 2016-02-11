# Variable Selection Client

The runner consists of two components

- mrat.py: Base varselect tool that logs to command line. Type 'python mrat.py' for usage.
- runner.py: Wrapper around mrat.py that pipes output to Cloudwatch and a log file. Usage, ./runner.py log-id params_for_mrat.py

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

```shell
docker run -v $PWD:/opt/MRAT_Refactor -it mrat bash
```

## Testing
To test outputs compare the output directories. In order to create predicatable outputs call to *improve* in rvarselect is set to use the same seed.

## Contributing

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [R Style Guide](https://google.github.io/styleguide/Rguide.xml)

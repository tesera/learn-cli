# Variable Selection Client

## Running

The runner consists of two components

- mrat.py: Base varselect tool that logs to command line. Type 'python mrat.py' for usage.
- runner.py: Wrapper around mrat.py that pipes output to Cloudwatch and a log file. Usage, ./runner.py log-id params_for_mrat.py

To run variable select inside docker container use the following command:

* `docker run -v $PWD:/opt/MRAT_Refactor -it mrat bash`

To test outputs compare the output directories. In order to create predicatable outputs call to *improve* in rvarselect is set to 
use the same seed.

## Style Guidelines
- [Python](https://www.python.org/dev/peps/pep-0008/)
- [R](https://google.github.io/styleguide/Rguide.xml)

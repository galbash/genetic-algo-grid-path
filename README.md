# Genetic Path Solver
## Requirements
* Python 3.8
* pip (Python package manager)

## Installing Dependencies
In the projects directory, run `pip install -r requirements.txt`. This command must be
executed in order to use the path solver, as it installs all the python dependencies it
uses.

## Running the Application
To run the application, simply `cd` to the project directory and run `python main.py`.
Output will be written to the `out` directory.

To list additional options, run `python main.py --help`.

You may have to set the `PYTHONPATH` to point to the project directory if you encounter
import errors

## Generating graphs
In order to re-generate graphs from execution data, execute `python graph_printer.py`.
Output will be written to the `out/graphs` directory.


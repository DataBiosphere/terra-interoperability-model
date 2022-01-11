# Data Model Exporter
## _Early prototype for converting RDF to JSON schema_

### Dependencies
You will need Python 3 and Poetry installed on your machine.

#### Python 3.9.1
_Download & Install:_ https://www.python.org/downloads/

#### Poetry
_Documentation:_ https://python-poetry.org/docs/


### SET UP
Initialize and configure the Poetry virtual environment:
```sh
cd tools/data-model-exporter  # Navigate to the data-model-exporter directory, where our Poetry config is (pyproject.toml)
poetry install
poetry run pre-commit install
```

### RUN THE SCRIPT

* Create a text file containing the list of classes that need to be pulled in the directory

* Navigate to the directory containing the script file:
```sh
cd tools/data-model-exporter/data_model_exporter
```

* Invoke the script using Poetry:
```sh
# run the script with a file of classes
poetry run ./dmExporter.py -f filepath -c /foo/bar/classes.txt
```

```sh
# run the script with a space-delimited list of classes
poetry run ./dmExporter.py -f filepath -l DataCollection BiomedicalResearch
```

This will create individual .json files for each schema converted.


### Troubleshooting
If Poetry commands are not working after installing Poetry, add this alias to your bash profile to ensure that Poetry is on your path:
```sh
export PATH=$PATH:$HOME/.poetry/bin
```

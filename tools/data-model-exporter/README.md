# Data Model Exporter
#### _Early prototype for converting RDF to JSON schema_

### Dependencies
#### _You will need Python3 and Poetry installed on your machine_
##### Python 3.9.1
###### _Download & Install:_ https://www.python.org/downloads/

##### Poetry
###### _Documentation:_ https://python-poetry.org/docs/


### SET UP
#### Install the Poetry vm and depedencies
```sh
cd [directory with .toml file]
poetry install
```

#### Create a txt file containing the list of classes that need to be pulled in the directory

###### Navigate to the directory containing the script file:
```sh
cd ../terra-interoperability-model/tools/data-model-exporter/data_model_exporter
```

#### Using poetry run the following command line:  
```py
# run the script with a file of classes
poetry run ./dmExporter.py -f "filepath" -c "class_name.txt"```py
# run the script with a list of classes
poetry run ./dmExporter.py -f "filepath" -l "DataCollection BiomedicalResearch"
```
###### _This will create individual json files for each schema converted_


#### Troubleshooting
###### _if poetry commands are not working after installing poetry, add this alias to your bash profile_
```sh
export PATH=$PATH:$HOME/.poetry/bin
```
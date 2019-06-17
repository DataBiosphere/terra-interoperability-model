#!/usr/bin/env python2

mport os
import argparse
import json


def make_new_dataset(dataset_name, dataset_description, parent_directory, output_name):
    """
    Gets JSON file(s) for assets, tables and relationships, combines them and then write the combined JSON to disk.
    :param dataset_name: the schema name for the dataset
    :param dataset_description: description of the schema
    :param parent_directory: the directory containing assets, relationships and tables JSON files
    :param output_name: the name of the output JSON, containing the combined assets, relationships and tables JSONs
    """
    dataset = init_dataset(dataset_name=dataset_name,
                           dataset_description=dataset_description)
    dataset_with_tables = add_to_schema(dataset,
                                        schema_type="tables",
                                        parent_directory=parent_directory,
                                        sub_directory="tables")
    dataset_with_relationships = add_to_schema(dataset_with_tables,
                                               schema_type="relationships",
                                               parent_directory=parent_directory,
                                               sub_directory="relationships")
    dataset_with_assets = add_to_schema(dataset_with_relationships,
                                        schema_type="assets",
                                        parent_directory=parent_directory,
                                        sub_directory="assets")
    save_dataset_as_json(dataset_with_assets,
                         output_name)


def init_dataset(dataset_name, dataset_description):
    """
    Creates any empty dataset as a dict that has a study name, description, and schema.
    :param dataset_name: the schema name for the dataset
    :param dataset_description: description of the schema
    """
    dataset = {
        "name": dataset_name,
        "description": dataset_description,
        "schema": {
            "tables": [],
            "relationships": [],
            "assets": []
        }
    }
    return dataset


def add_to_schema(dataset, schema_type, parent_directory,  sub_directory):
    """
    Adds JSON files to the current dataset as a dict.
    :param dataset: the combined dataset to be written to disk
    :param schema_type: which part of the data set is being added to the schema, (either assets, relationships or tables)
    :param parent_directory: the directory containing assets, relationships and tables JSON files
    :param sub_directory: the child directory of either assets or tables JSON files
    """
    json_files_path = os.path.join(parent_directory, sub_directory)
    for file in os.listdir(json_files_path):
        if file.endswith(".json"):
            with open(os.path.join(json_files_path, file), "r") as json_file:
                json_as_dict = json.load(json_file)
            dataset["schema"][schema_type].append(json_as_dict)
    return dataset


def save_dataset_as_json(dataset, output_name):
    """
    Writes the combined JSON of assets, tables and relationships to disk.
    :param dataset: the combined dataset to be written to disk
    :param output_name: the name of the output JSON, containing the combined assets, relationships and tables JSONs
    """
    with open(output_name, "w") as output_file:
        json.dump(dataset,
                  output_file,
                  sort_keys=False,
                  indent=2)


if __name__ == "__main__":
    # get the argument inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-name",
                        "-n",
                        dest="dataset_name",
                        required=True,
                        help="the schema name for the dataset")
    parser.add_argument("--dataset-description",
                        "-d",
                        dest="dataset_description",
                        required=True,
                        help="description of the schema")
    parser.add_argument("--input-directory",
                        "-i",
                        dest="input_directory",
                        required=True,
                        help="the directory containing assets, relationships and tables JSON files")
    parser.add_argument("--output-name",
                        "-o",
                        dest="output_name",
                        required=True,
                        help="the name of the output JSON, containing the combined assets, relationships and tables")
    args = parser.parse_args()

    make_new_dataset(dataset_name=args.dataset_name,
                     dataset_description=args.dataset_description,
                     parent_directory=args.input_directory,
                     output_name=args.output_name)

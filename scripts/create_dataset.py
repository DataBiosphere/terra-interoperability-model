#!/usr/bin/env python2
import os
import argparse
import json


def make_new_dataset(dataset_name, dataset_description, input_tables_directory, input_assets_directory, output_name):
    """
    Adds JSON files for assets and tables to a dataset, generates relationships and then writes the final JSON to disk.
    :param dataset_name: the schema name for the dataset
    :param dataset_description: description of the schema
    :param input_tables_directory: the directory containing tables JSON files
    :param input_assets_directory: the directory containing assets JSON files
    :param output_name: the name of the output JSON, containing the combined assets, relationships and tables JSONs
    """
    input_tables = get_json(parent_directory=input_tables_directory)
    tables, relationships = create_tables_and_relationships(input_tables=input_tables)

    input_assets = get_json(parent_directory=input_assets_directory)
    assets = [
        {
            "name": input_assets[input_asset_name]["name"],
            "rootTable": input_assets[input_asset_name]["rootTable"],
            "rootColumn": input_assets[input_asset_name]["rootColumn"],
            "tables": [{"name": table["name"], "columns": []} for table in tables],
            "follow": [relationship["name"] for relationship in relationships]
        } for input_asset_name in input_assets
    ]

    dataset = {
        "name": dataset_name,
        "description": dataset_description,
        "schema": {"tables": tables, "relationships": relationships, "assets": assets}
    }
    save_dataset_as_json(dataset=dataset, output_name=output_name)


def get_json(parent_directory):
    """
    Adds JSON files to a dict with each key being the name field of a json file.
    and the value being the corresponding json.
    :param parent_directory: the directory containing JSON files to add to the dict
    """
    input_dict = {}
    for file in os.listdir(parent_directory):
        if file.endswith(".json"):
            with open(os.path.join(parent_directory, file), "r") as json_file:
                json_as_dict = json.load(json_file)
            # add the name field field of the json as a key to make each json searchable
            input_dict[json_as_dict["name"]] = json_as_dict
    return input_dict


def create_tables_and_relationships(input_tables):
    """
    Creates tables and relationships from the input tables
    :param input_tables: the input json tables that have been added to a dict
    """
    tables, relationships = [], []
    for input_table_name in input_tables:
        table, new_relationships = create_table_and_relationships(input_table=input_tables[input_table_name],
                                                                  input_tables=input_tables)
        tables.append(table)
        relationships.extend(new_relationships)

    return tables, relationships


def create_table_and_relationships(input_table, input_tables):
    """
    Creates a table and relationships using the input tables fields and reference field.
    :param input_table: the input table to be used to create a new table and relationships
    :param input_tables: the input tables that have been added to a dict and used to validate the created relationships
    """

    input_table_name = input_table["name"]
    columns, table_relationships = [], []
    for input_column in input_table["columns"]:
        column, new_relationships = create_column_and_relationships(input_relationships=input_column.get("links"),
                                                                    column_name=input_column["name"],
                                                                    column_datatype=input_column["datatype"],
                                                                    column_array_of=input_column.get("array_of"),
                                                                    input_table_name=input_table_name,
                                                                    input_tables=input_tables)
        columns.append(column)
        table_relationships.extend(new_relationships)

    table = {"name": input_table_name, "columns": columns}

    return table, table_relationships


def create_column_and_relationships(input_relationships,
                                    column_name,
                                    column_datatype,
                                    column_array_of,
                                    input_table_name,
                                    input_tables):
    """
    Creates a column and relationships, keeping ony the name, data type and column field from the input column.
    :param input_relationships: the list of relationships from an input JSON column
    :param column_name: the name of the input JSON column
    :param column_datatype: the primitive type enforced for values of the input JSON column
    :param column_array_of: indicates if the column values should be in array
    :param input_table_name: the name of input JSON table that has the input_column
    :param input_tables: the input tables that have been added to a dict and used to validate the created relationships
    """
    relationships = []
    if input_relationships:
        if not any([validate_table_and_column(table_name=input_relationship["table_name"],
                                              column_name=input_relationship["column_name"],
                                              column_datatype=column_datatype,
                                              input_tables=input_tables)
                    for input_relationship in input_relationships]):
            raise SystemExit("Error: The relationship(s) provided for table, {}, column {} are not valid"
                             .format(input_table_name, column_name))

        relationships = [
            {
                "name": "{}_{}_to_{}_{}".format(input_table_name,
                                                column_name,
                                                input_relationship["table_name"],
                                                input_relationship["column_name"]),
                "from": {"table": input_table_name, "column": column_name, "cardinality": "one"},
                "to": {
                        "table": input_relationship["table_name"],
                        "column": input_relationship["column_name"],
                        "cardinality": "many" if column_array_of else "one"
                      }
            }
            for input_relationship in input_relationships]

    column = {
        "name": column_name,
        "datatype": column_datatype,
        "array_of": column_array_of is True
    }

    return column, relationships


# TODO add validation for duplicate assets, tables, columns and relationships
def validate_table_and_column(table_name, column_name, column_datatype, input_tables):
    """
    Validates a relationship checking the the given table and column exist in input tables and the datatype is correct.
    :param table_name: the name of table containing has the input_column that will be validated against the input tables
    :param column_name: the name of the input_column that will be validated against the input tables
    :param column_datatype: the primitive type enforced for values of the input JSON column
    :param input_tables: the input tables that have been added to a dict and used to validate the created relationships
    """
    for input_table_name in input_tables:
        if input_table_name == table_name:
            for input_column in input_tables[input_table_name]["columns"]:
                if input_column["name"] == column_name:
                    return input_column["datatype"] == column_datatype

    return False


def save_dataset_as_json(dataset, output_name):
    """
    Writes the combined JSON of assets, tables and relationships to disk.
    :param dataset: the combined dataset to be written to disk
    :param output_name: the name of the output JSON, containing the combined assets, relationships and tables JSONs
    """
    with open(output_name, "w") as output_file:
        json.dump(dataset, output_file, sort_keys=False, indent=2)


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
    parser.add_argument("--input-tables-directory",
                        "-t",
                        dest="input_tables_directory",
                        required=True,
                        help="the directory containing tables JSON files")
    parser.add_argument("--input-assets-directory",
                        "-a",
                        dest="input_assets_directory",
                        required=True,
                        help="the directory containing assets JSON file(s)")
    parser.add_argument("--output-name",
                        "-o",
                        dest="output_name",
                        required=True,
                        help="the name of the output JSON, containing the combined assets, relationships and tables")
    args = parser.parse_args()

    make_new_dataset(dataset_name=args.dataset_name,
                     dataset_description=args.dataset_description,
                     input_tables_directory=args.input_tables_directory,
                     input_assets_directory=args.input_assets_directory,
                     output_name=args.output_name)

#!/usr/bin/env python

"""Create a basic CLI tool that parses the arg list defined in the spec
(as linked in the parent epic) and hands off the args to a stub driver method
"""

import argparse
import json
import logging
from os import path

from data_model_exporter.ttl_schema_generator import JsonSchema, TtlSchemaGenerator


def get_arguments() -> tuple[str, list[str]]:
    """Arguments defined in spec
    1) a path to the data model *.TTL file
    2) a "class file" (newline delimited list of strings that correspond to RDF classes)
    """
    parser = argparse.ArgumentParser(description='Process data model export')
    parser.add_argument(
        '-f',
        '--file-path',
        help="path to the data model e.g.: 'src/terra-core/TerraDCAT-AP.ttl'",
        required=True)
    class_list_source = parser.add_mutually_exclusive_group(required=True)
    class_list_source.add_argument(
        '-l',
        '--class-list',
        nargs='+',
        help="a class listing string e.g.: 'DataCollection BiomedicalResearch'")
    class_list_source.add_argument('-c', '--class-path', help="a class listing file e.g.: 'class_name.txt'")
    args = parser.parse_args()

    if args.class_list:
        return args.file_path, args.class_list
    else:
        with open(args.class_path, 'r') as class_file:
            class_list = [
                line.strip()
                for line in class_file
                if line.strip() != ""
            ]
        logging.info(f"{len(class_list)} classes parsed from {args.class_path}")
        logging.info(f"class_list: {class_list}")
        return args.file_path, class_list


def rdf_to_json(file_path: str, class_list: list[str]) -> dict[str, JsonSchema]:
    """
    Function to convert RDF to JSON and store the class names with their schemas in a dictionary
    :param file_path: File Path to RDF
    :param class_list: List of classes to parse
    :return: Dictionary {key=class_name : value=json_schema}
    """
    json_schema_list = {
        class_name: TtlSchemaGenerator(class_name, file_path).build_schema()
        for class_name in class_list
    }
    return json_schema_list


def write_to_json(out_file_name: str, json_dict: dict[str, JsonSchema], key: str) -> None:
    logging.info(json.dumps(json_dict[key], indent=4))

    with open(out_file_name, 'w') as f:
        json.dump(json_dict[key], f)


def main() -> None:
    # get CLI arguments
    file_path, class_list = get_arguments()
    # invoke driver to transform RDF to JSON
    json_dict = rdf_to_json(file_path, class_list)
    # write one file per class provided
    for key in json_dict:
        out_file_name = f"{key}.json"
        if path.exists(out_file_name):
            rewrite = input(out_file_name + " already exists. Overwrite? (y/n)")
            if rewrite == "y":
                write_to_json(out_file_name, json_dict, key)
        else:
            write_to_json(out_file_name, json_dict, key)


if __name__ == "__main__":
    main()

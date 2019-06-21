#!/usr/bin/env python2

import os
import unittest
import tempfile
from scripts import create_dataset
import json
from deepdiff import DeepDiff
import errno


class CreateDatasetTest(unittest.TestCase):
    def test_make_new_dataset(self):
        # file paths for truth files
        current_file_dir = os.path.dirname(__file__)
        truth_output_schema_json = os.path.join(current_file_dir, "input_files/test_input_dataset.json")

        # generate temp file names for output files
        output_dataset = os.path.join(tempfile.mkdtemp(), 'test_output_dataset')

        # run the create dataset python script with given input JSON files
        create_dataset.make_new_dataset(dataset_name="dataset_name",
                                        dataset_description="dataset_description",
                                        input_tables_directory=os.path.join(current_file_dir, "input_files/tables"),
                                        input_assets_directory=os.path.join(current_file_dir, "input_files/assets"),
                                        output_name=output_dataset)

        # compare expected outputs from python script to truth files
        with open(truth_output_schema_json, "r") as truth_file:
            with open(output_dataset, "r") as output_file:
                output_dict = json.load(output_file)
                truth_dict = json.load(truth_file)
        ddiff = DeepDiff(output_dict, truth_dict, ignore_order=True)

        # if there are differences
        self.assertTrue(len(ddiff) == 0,
                        "Error: The created json is not equal to truth file\n{}".format(ddiff))

    def test_validate_table_and_column(self):
        current_file_dir = os.path.dirname(__file__)
        input_tables = create_dataset.get_json(os.path.join(current_file_dir, "input_files/tables"))

        # check an expected valid table and column pair
        self.assertTrue(create_dataset.validate_table_and_column(table_name="table_2",
                                                                 column_name="column_1",
                                                                 column_datatype="string",
                                                                 input_tables=input_tables),
                        "Error: The valid table and column could not be validated using input JSON tables")

        # check an expected invalid input column datatype
        self.assertFalse(create_dataset.validate_table_and_column(table_name="table_2",
                                                                  column_name="column_1",
                                                                  column_datatype="float",
                                                                  input_tables=input_tables),
                        "Error: The invalid input column datatype was validated using input JSON tables")

        # check an expected invalid table name
        self.assertFalse(create_dataset.validate_table_and_column(table_name="invalid_table_name",
                                                                  column_name="column_1",
                                                                  column_datatype="string",
                                                                  input_tables=input_tables),
                         "Error: The invalid table name was validated using input JSON tables")

        # check an expected invalid column name
        self.assertFalse(create_dataset.validate_table_and_column(table_name="table_4",
                                                                  column_name="invalid_column_name",
                                                                  column_datatype="string",
                                                                  input_tables=input_tables),
                         "Error: The invalid column name was validated using input JSON tables")

        invalid_input_tables = create_dataset.get_json(os.path.join(current_file_dir, "input_files/invalid_tables"))
        # check a invalid relationship with two columns containing two different datatype
        self.assertFalse(create_dataset.validate_table_and_column(table_name="table_2",
                                                                  column_name="column_1",
                                                                  column_datatype="float",
                                                                  input_tables=invalid_input_tables),
                         "Error: The invalid relationship with 2 columns containing 2 different datatype was validated")


if __name__ == '__main__':
    unittest.main()

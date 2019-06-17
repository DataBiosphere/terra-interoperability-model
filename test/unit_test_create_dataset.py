#!/usr/bin/env python2

import os
import unittest
import tempfile
from scripts.create_dataset import make_new_dataset
import json
from deepdiff import DeepDiff


class CreateDatasetTest(unittest.TestCase):
    def test_files(self):
        # file paths for truth files
        current_file_dir = os.path.dirname(__file__)
        truth_output_schema_json = os.path.join(current_file_dir, "input_files/test_input_dataset.json")

        # generate temp file names for output files
        output_dataset = os.path.join(tempfile.mkdtemp(), 'test_output_dataset')

        # run the create dataset python script with given input JSON files
        make_new_dataset(dataset_name="dataset_name",
                         dataset_description="dataset_description",
                         parent_directory=os.path.join(current_file_dir, "input_files"),
                         output_name=output_dataset)

        # compare expected outputs from python script to truth files
        with open(truth_output_schema_json, "r") as truth_file:
            with open(output_dataset, "r") as output_file:
                output_dict = json.load(output_file)
                truth_dict = json.load(truth_file)
        ddiff = DeepDiff(output_dict, truth_dict, ignore_order=True)

        self.assertTrue(len(ddiff) == 0,
                        "Error: The created json is not equal to truth file")



if __name__ == '__main__':
    unittest.main()

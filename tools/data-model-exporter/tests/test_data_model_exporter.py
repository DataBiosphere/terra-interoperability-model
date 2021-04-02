#!/usr/bin/env python
import unittest
from unittest.mock import patch

import sys
import os
import json
from collections import OrderedDict

from data_model_exporter.dmExporter import get_arguments, extract, rdf_to_json

# Test Fixtures (defaults to test)
# todo: remove extraneous fixtures after testing
test_file_path = "../../src/terra-core/TerraDCAT-AP.ttl"
test_class = "DataCollection"
test_class_list = "DataCollection DataSnapshot"
# todo: toy TTL string used for fixture data
test_ttl_file = os.path.join(os.path.dirname(__file__), 'DataCollection.ttl')
test_json_file = os.path.join(os.path.dirname(__file__), 'DataCollection.json')
with open(test_json_file) as f:
    test_json = f.readline()

# todo: Just load the Terra TIM TTL files and assert those serialize to a known good format?
# todo: should this be snake_case?
class DataModelExporterTestCase(unittest.TestCase):

    def test_extract(self):
        """
        Test for extracting RDF from ttl files
        """
        json_schema_dict = {}
        json_schema_dict[test_class] = extract(test_ttl_file,test_class)
        serialized_json = json.dumps(json_schema_dict[test_class])
        self.assertEqual(OrderedDict(serialized_json), OrderedDict(test_json))

        import pdb; pdb.set_trace()
        pass
        #self.assertEqual(), json.loa
        #import pdb ; pdb.set_trace()

    # todo: ensure it serializes to JSON schema properly
    # AssertionError: {'DataCollection': {'$id': rdflib.term.UR[2255 chars]y']}} != '{"$id": "http://datamodel.terra.bio/Terr[1929 chars]r"]}'
     def test_rdf_to_json(self):
         """
         Test for transforming RDF to JSON
         """
         self.assertEqual(rdf_to_json(test_ttl_file,test_class_list), test_json)

# todo: These should run as part of CI (triggered by a github action)
# use validate-python from hca-ingest as a model:
# - checkout
# - install python +  poetry + deps
# - run tests

if __name__ == '__main__':
    unittest.main()
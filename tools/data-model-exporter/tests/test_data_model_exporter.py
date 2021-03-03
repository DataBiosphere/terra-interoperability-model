#!/usr/bin/env python
import unittest
#from data_model_exporter.dmExporter import get_arguments, extract, rdf_to_json

# Test Fixtures (defaults to test)
#Terra = Namespace("http://datamodel.terra.bio/TerraDCAT_ap#")
# the builtin RDFLIB PROV NS does not define 'definition' for unknown reasons, hence this ad hoc def
#Prov = Namespace("http://www.w3.org/ns/prov#")

file_path = "../../src/terra-core/TerraDCAT-AP.ttl"
class_list = "DataCollection"

# todo: should this be snake_case?
class DataModelExporterTestCase(unittest.TestCase):
    def test_get_arguments(self):
        """
        Simple test for getting arguments from the command line
        def set_up(self):
            self.parser = create_parser()
        """
        def test_examples(self):
            parsed = self.parser.parse_args(['--file_path', file_path], ['--class_list', class_list])
            self.assertTrue(parsed.file_path, '../../src/terra-core/TerraDCAT-AP.ttl')
            self.assertTrue(parsed.class_list, 'XXXX')
        print ("TESTED test_get_arguments!")

    def test_rdf_to_json(self):
        """
        Simple test for transforming RDF to JSON
        """
        #result = self.run_pipeline(stage_data, config_name="test_stage_data.yaml")
        #self.assertTrue(result.success)
        print ("running test_rdf_to_json!")


if __name__ == '__main__':
    unittest.main()
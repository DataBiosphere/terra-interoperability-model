#!/usr/bin/env python
import unittest
from data_model_exporter.dmExporter import get_arguments, extract, rdf_to_json

# Test Fixtures (defaults to test)
#Terra = Namespace("http://datamodel.terra.bio/TerraDCAT_ap#")
#the builtin RDFLIB PROV NS does not define 'definition' for unknown reasons, hence this ad hoc def
#Prov = Namespace("http://www.w3.org/ns/prov#")

file_path = "../../../src/terra-core/TerraDCAT-AP.ttl"
class_name = "DataCollection"

data_collection = """{"$id": "http://datamodel.terra.bio/TerraDCAT_ap#DataCollection", "$schema": "http://json-schema.org/draft-07/schema#/", "title": "DataCollection", "description": "Extension of DCAT:Catalog to support Data Use Ontology terms and set required properties for DSP DCAT Application Profile. A collection of one or more DSPdcat_ap:Datasets or DSPdcat_apDataCollections.", "definitions": {}, "type": "object", "additionalProperties": true, "properties": {"describedBy": {"description": "The URL reference to the JSON Schema that defines this object.", "type": "string"}, "id": {"description": "UUID for this entity.", "type": "string"}, "dct:issued": {"description": "dct:issued", "$ref": null}, "dct:publisher": {"description": "dct:publisher", "$ref": null}, "dct:description": {"description": "dct:description", "$ref": null}, "TerraDCAT_ap:hasDataUseRequirement": {"description": "TerraDCAT_ap:hasDataUseRequirement", "$ref": "http://purl.obolibrary.org/obo/DUO_0000017"}, "TerraDCAT_ap:hasDataCollection": {"description": "TerraDCAT_ap:hasDataCollection", "$ref": "http://datamodel.terra.bio/TerraDCAT_ap#DataCollection"}, "TerraDCAT_ap:hasDataset": {"description": "TerraDCAT_ap:hasDataset", "$ref": "http://datamodel.terra.bio/TerraDCAT_ap#Dataset"}, "dct:creator": {"description": "dct:creator", "$ref": null}, "dct:modified": {"description": "dct:modified", "$ref": null}, "TerraDCAT_ap:hasDataUseLimitation": {"description": "TerraDCAT_ap:hasDataUseLimitation", "$ref": "http://purl.obolibrary.org/obo/DUO_0000001"}, "dcat:themeTaxonomy": {"description": "dcat:themeTaxonomy", "$ref": null}, "dcat:theme": {"description": "dcat:theme", "$ref": null}, "dct:title": {"description": "dct:title", "$ref": null}, "TerraDCAT_ap:hasDataSnapshot": {"description": "TerraDCAT_ap:hasDataSnapshot", "$ref": "http://datamodel.terra.bio/TerraDCAT_ap#DataSnapshot"}}, "required": ["id", "describedBy", "dct:issued", "dct:publisher", "dct:description", "dct:creator", "dct:modified"]}"""


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
        self.assertEqual(rdf_to_json(file_path,class_list),"DataCollection")
        #result = self.run_pipeline(stage_data, config_name="test_stage_data.yaml")
        #self.assertTrue(result.success)
        # print ("running test_rdf_to_json!")

    def test_extract(self):
        self.assertEqual(extract(file_path,class_name),"../../DataCollection.json")
        import pdb ; pdb.set_trace()





if __name__ == '__main__':
    unittest.main()
import copy
import os
import unittest

import rdflib

from data_model_exporter.ttl_schema_generator import TtlSchemaGenerator
from data_model_exporter.property_types import PrimitiveType, RefType


class TtlSchemaGeneratorTestCase(unittest.TestCase):
    def fixture_path(self, filename):
        return os.path.join(os.path.dirname(__file__), 'fixtures', filename)

    def setUp(self):
        self.generator = TtlSchemaGenerator('Zombocom', self.fixture_path('test.ttl'))
        self.generator.build_schema()

    def test_primary_namespace_detects_correct_namespace(self):
        self.assertEqual('https://zombo.com/zombo#', str(self.generator.primary_namespace))

    def test_ensure_property_initialized_is_idempotent_and_initializes_property(self):
        zombo_node = rdflib.term.URIRef("https://zombo.com/zombo#possibilities")
        self.generator.ensure_property_initialized(zombo_node)
        self.assertIn("zombo:possibilities", self.generator.schema.properties)
        first_execution = copy.deepcopy(self.generator.schema.properties['zombo:possibilities'])
        self.generator.ensure_property_initialized(zombo_node)
        self.assertEqual(first_execution, self.generator.schema.properties['zombo:possibilities'])

    def test_annotates_schema_with_various_flat_fields(self):
        self.assertEqual(self.generator.schema.description, "This is Zombocom.")
        self.assertEqual(self.generator.schema.title, "ZomboLabel")
        self.assertEqual(self.generator.schema.skos_preflabel, "ZomboPrefLabel")

    def test_annotates_from_domain_fields(self):
        self.assertIn('zombo:redundancy', self.generator.schema.properties)
        this_is_zombocom = self.generator.schema.properties['zombo:redundancy']
        self.assertEqual(this_is_zombocom.description, "Yes, this is Zombocom.")

    def test_annotates_enumerated_ranges_on_property(self):
        self.assertIn('zombo:greeting', self.generator.schema.properties)
        enum_values = self.generator.schema.properties['zombo:greeting'].allowed_values
        self.assertEqual(enum_values, [
            "Welcome to Zombocom.",
            "This is Zombocom."
        ])

    def test_does_not_annotate_properties_on_other_classes(self):
        self.assertNotIn('zombo:abilityToDoAnything', self.generator.schema.properties)

    def test_annotates_one_cardinality_as_required(self):
        self.assertIn('zombo:limit', self.generator.schema.properties)
        the_only_limit = self.generator.schema.properties['zombo:limit']
        self.assertTrue(the_only_limit.required)

    def test_annotates_somevaluesfrom_as_array(self):
        self.assertIn('zombo:redundancy', self.generator.schema.properties)
        this_is_zombocom = self.generator.schema.properties['zombo:redundancy']
        self.assertEqual(this_is_zombocom.allowed_types, [PrimitiveType('string')])
        redundancy_dict = this_is_zombocom.as_dict()
        self.assertEqual(redundancy_dict['type'], 'array')
        self.assertEqual(redundancy_dict['items'], {'type': 'string'})

    def test_annotates_allvaluesfrom_as_type(self):
        self.assertIn('zombo:limit', self.generator.schema.properties)
        the_only_limit = self.generator.schema.properties['zombo:limit']
        self.assertEqual(the_only_limit.allowed_types, [RefType('zombo:Yourself')])
        self.assertEqual(the_only_limit.as_dict()['$ref'], 'zombo:Yourself')

    def test_annotates_cardinality_limits_as_array_type(self):
        self.assertIn('zombo:possibilities', self.generator.schema.properties)
        infinite_possibilities = self.generator.schema.properties['zombo:possibilities']
        self.assertEqual(infinite_possibilities.min_cardinality, 1)
        self.assertTrue(infinite_possibilities.is_array_type())

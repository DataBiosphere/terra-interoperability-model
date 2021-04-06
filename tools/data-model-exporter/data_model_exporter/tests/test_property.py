import unittest

from data_model_exporter.property import Property
from data_model_exporter.property_types import PrimitiveType, RefType


class PropertyTestCase(unittest.TestCase):
    def test_is_array_type_true_if_either_cardinality(self):
        self.assertTrue(Property("foo", "desc", min_cardinality=1).is_array_type())
        self.assertTrue(Property("foo", "desc", max_cardinality=3).is_array_type())

    def test_is_array_type_false_if_neither_cardinality(self):
        self.assertFalse(Property("foo", "desc").is_array_type())

    def test_add_type_adds_type(self):
        prop = Property("foo", "desc")
        self.assertEqual(len(prop.allowed_types), 0)
        prop.add_type(PrimitiveType("string"))
        self.assertEqual(prop.allowed_types, [PrimitiveType("string")])

    def test_add_type_blocks_further_types_if_restrictive(self):
        prop = Property("foo", "desc")
        prop.add_type(PrimitiveType("string"), restrictive=True)
        with self.assertRaises(ValueError):
            prop.add_type(RefType("argbl"))

    def test_add_type_allows_further_types_if_not_restrictive(self):
        prop = Property("foo", "desc")
        prop.add_type(PrimitiveType("string"), restrictive=False)
        # we just run this to see if it raises an exception, so there's no assertions in the test
        prop.add_type(RefType("argbl"))

    def test_add_type_mutex_with_allowed_values(self):
        prop = Property("foo", "desc")
        prop.add_type(PrimitiveType("string"))
        with self.assertRaises(ValueError):
            prop.add_enum_value("steve")

    def test_add_type_ignores_duplicates(self):
        prop = Property("foo", "desc")
        prop.add_type(PrimitiveType("string"))
        prop.add_type(PrimitiveType("string"))
        self.assertEqual(prop.allowed_types, [PrimitiveType("string")])

    def test_add_enum_value_adds_enum_value(self):
        prop = Property("foo", "desc")
        prop.add_enum_value("steve")
        self.assertEqual(prop.allowed_values, ["steve"])

    def test_add_enum_value_mutex_with_type_constraints(self):
        prop = Property("foo", "desc")
        prop.add_enum_value("steve")
        with self.assertRaises(ValueError):
            prop.add_type(PrimitiveType("string"))

    def test_optional_fields_includes_only_defined_fields(self):
        prop = Property(
            "foo",
            "desc",
            comment="hey",
            skos_preflabel="jimbo"
        )

        optional_fields = prop.optional_fields()
        self.assertIn("comment", optional_fields)
        self.assertIn("skos:prefLabel", optional_fields)
        self.assertNotIn("title", optional_fields)
        self.assertNotIn("oneOf", optional_fields)

    def test_base_type_info_defaults_to_string(self):
        prop = Property("foo", "desc")
        self.assertEqual(prop.base_type_info(), {'type': 'string'})

    def test_base_type_info_returns_type_for_single_value(self):
        prop = Property("foo", "desc")
        prop.add_type(RefType("reef"))
        self.assertEqual(prop.base_type_info(), {'$ref': 'reef'})

    def test_base_type_info_returns_oneof_for_multiple_values(self):
        prop = Property("foo", "desc")
        prop.add_type(RefType("ref1"))
        prop.add_type(RefType("ref2"))
        self.assertEqual(prop.base_type_info(), {
            'oneOf': [
                {'$ref': 'ref1'},
                {'$ref': 'ref2'},
            ]
        })

    def test_type_info_generates_flat_type_info_if_not_array(self):
        prop = Property("foo", "desc")
        prop.add_type(RefType("reef"))
        self.assertEqual(prop.type_info(), {'$ref': 'reef'})

    def test_type_info_wraps_in_array_if_array(self):
        prop = Property("foo", "desc", min_cardinality=0)
        prop.add_type(RefType("reef"))
        self.assertEqual(prop.type_info(), {
            'type': 'array',
            'items': {'$ref': 'reef'},
        })

    def test_as_dict_includes_expected_fields(self):
        prop = Property("foo", "desc", max_cardinality=3)
        prop.add_enum_value("steve")
        prop.add_enum_value("stove")
        expected_fields = {
            'description': 'desc',
            'oneOf': ['steve', 'stove'],
            'type': 'array',
            'items': {'type': 'string'},
            'maxItems': 3,
        }
        dictified = prop.as_dict()
        for expected_field, expected_value in expected_fields.items():
            self.assertIn(expected_field, dictified)
            self.assertEqual(dictified[expected_field], expected_value)

    def test_as_dict_always_includes_description_even_if_blank(self):
        prop = Property("foo", "", max_cardinality=3)
        self.assertIn('description', prop.as_dict())

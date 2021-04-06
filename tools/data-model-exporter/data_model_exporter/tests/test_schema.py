import unittest

from data_model_exporter.property import Property
from data_model_exporter.schema import Schema


class SchemaTestCase(unittest.TestCase):
    def test_optional_fields_includes_only_defined_fields(self):
        schema = Schema(
            "term_name",
            skos_preflabel="preferred",
            exact_synonym=["splynonym"])

        fields = schema.optional_fields()
        self.assertIn('skos:prefLabel', fields)
        self.assertIn('skos:exactMatch', fields)
        self.assertNotIn('title', fields)
        self.assertNotIn('owl:equivalentClass', fields)
        self.assertNotIn('rdfs:subClassOf', fields)

    def test_required_property_names_includes_only_required_properties(self):
        schema = Schema(
            "term_name",
            properties={
                'mandatory': Property('mandatory', 'desc', required=True),
                'whatever_man': Property('whatever_man', 'desc', required=False),
            }
        )

        self.assertEqual(schema.required_property_names(), ['mandatory'])

    def test_as_dict_includes_expected_fields(self):
        schema = Schema(
            "term_name",
            properties={
                'mandatory': Property('mandatory', 'desc', required=True),
                'whatever_man': Property('whatever_man', 'desc', required=False),
            },
            skos_preflabel="preferred",
            exact_synonym=["splynonym"])

        expected_fields = {
            '$id': 'term_name',
            'type': 'object',
            'additionalProperties': True,
            'properties': {
                'mandatory': {
                    'description': 'desc',
                    'type': 'string'
                },
                'whatever_man': {
                    'description': 'desc',
                    'type': 'string'
                },
            },
            'required': ['mandatory']
        }
        schema_dict = schema.as_dict()

        for expected_field, expected_value in expected_fields.items():
            self.assertIn(expected_field, schema_dict)
            self.assertEqual(schema_dict[expected_field], expected_value)

    def test_as_dict_always_includes_description_even_if_blank(self):
        schema = Schema("term", description="")
        self.assertIn("description", schema.as_dict())

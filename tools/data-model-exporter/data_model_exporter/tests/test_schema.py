import unittest

from data_model_exporter.schema import Schema


class SchemaTestCase(unittest.TestCase):
    def test_optional_fields_includes_only_defined_fields(self):
        pass

    def test_required_property_names_includes_only_required_properties(self):
        pass

    def test_as_dict_includes_expected_fields(self):
        pass

    def test_as_dict_always_includes_description_even_if_blank(self):
        pass

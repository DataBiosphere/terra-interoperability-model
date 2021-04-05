import unittest

from data_model_exporter.property import Property


class PropertyTestCase(unittest.TestCase):
    def test_is_array_type_true_if_either_cardinality(self):
        self.assertTrue(Property("foo", "desc", min_cardinality=1).is_array_type())

    def test_is_array_type_false_if_neither_cardinality(self):
        self.assertFalse(Property("foo", "desc").is_array_type())

    def test_add_type_adds_type(self):
        pass

    def test_add_type_blocks_further_types_if_restrictive(self):
        pass

    def test_add_type_allows_further_types_if_not_restrictive(self):
        pass

    def test_add_type_mutex_with_allowed_values(self):
        pass

    def test_add_type_ignores_duplicates(self):
        pass

    def test_add_enum_value_adds_enum_value(self):
        pass

    def test_add_enum_value_mutex_with_type_constraints(self):
        pass

    def test_optional_fields_includes_only_defined_fields(self):
        pass

    def test_base_type_info_defaults_to_string(self):
        pass

    def test_base_type_info_returns_type_for_single_value(self):
        pass

    def test_base_type_info_returns_oneof_for_multiple_values(self):
        pass

    def test_type_info_generates_flat_type_info_if_not_array(self):
        pass

    def test_type_info_wraps_in_array_if_array(self):
        pass

    def test_as_dict_includes_expected_fields(self):
        pass

    def test_as_dict_always_includes_description_even_if_blank(self):
        pass

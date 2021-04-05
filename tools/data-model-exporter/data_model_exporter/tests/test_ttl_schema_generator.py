import unittest

from data_model_exporter.ttl_schema_generator import TtlSchemaGenerator


class TtlSchemaGeneratorTestCase(unittest.TestCase):
    def test_primary_namespace_detects_correct_namespace(self):
        pass

    def test_ensure_property_initialized_is_idempotent_and_initializes_property(self):
        pass

    def test_annotates_schema_with_various_flat_fields(self):
        pass

    def test_annotates_from_restriction_properties(self):
        pass

    def test_annotates_property_with_various_flat_fields(self):
        pass

    def test_annotates_from_domain_fields(self):
        pass

    def test_annotates_enumerated_ranges_on_property(self):
        pass

    def test_annotates_various_ref_fields(self):
        pass

    def test_annotates_one_cardinality_as_required(self):
        pass

    def test_annotates_somevaluesfrom_as_oneof(self):
        pass

    def test_annotates_allvaluesfrom_as_type(self):
        pass

    def test_annotates_cardinality_limits_as_array_type(self):
        pass

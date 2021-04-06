import os
import unittest

from rdflib import Graph

from data_model_exporter.rdf_graph_manager import RdfGraphManager


class RdfGraphManagerTestCase(unittest.TestCase):
    def fixture_path(self, filename):
        return os.path.join(os.path.dirname(__file__), 'fixtures', filename)

    def setUp(self):
        # parse in the graph in the ttl file
        with open(self.fixture_path('test.ttl'), 'r') as ttl_file:
            self.graph = Graph().parse(ttl_file, format='turtle')
        self.graph_manager = RdfGraphManager(self.graph)

    def test_primary_namespace_detects_correct_namespace(self):
        self.assertEqual('https://zombo.com/zombo#', str(self.graph_manager.primary_namespace))

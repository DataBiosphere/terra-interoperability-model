from dataclasses import dataclass

from cached_property import cached_property
import rdflib
from rdflib import Graph, Namespace

from .property_types import PrimitiveType, RefType
from .typing import PropertyType, RdfNodeName

PRIMITIVE_TYPES = {
    'xsd:string': 'string',
    'xsd:anyURI': 'string',
}


# helper functions to perform common translations between RDF graphs and our data model
@dataclass
class RdfGraphManager:
    graph: Graph

    def namespaced_name_for_node(self, node: rdflib.term.Identifier) -> RdfNodeName:
        name: str = node.n3(self.graph.namespace_manager)  # hardcoding type for type annotations
        return RdfNodeName(name)

    def type_annotation_to_property_type(self, node: rdflib.term.Identifier) -> PropertyType:
        if isinstance(node, rdflib.term.URIRef):
            namespaced_name = self.namespaced_name_for_node(node)
            if namespaced_name in PRIMITIVE_TYPES:
                return PrimitiveType(PRIMITIVE_TYPES[namespaced_name])

            return RefType(namespaced_name)

        raise ValueError(f"Unrecognized type annotation {node}")

    @cached_property
    def primary_namespace(self) -> Namespace:
        # primary namespace for a graph is listed both under its actual namespace
        # and under the 'empty string' namespace
        namespace_uriref = dict([namespace for namespace in self.graph.namespaces()])['']

        return Namespace(str(namespace_uriref))

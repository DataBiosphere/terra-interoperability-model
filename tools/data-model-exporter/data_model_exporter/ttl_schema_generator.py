from dataclasses import dataclass, field
import logging

from cached_property import cached_property
import rdflib
from rdflib import Graph, Namespace, RDF, RDFS, OWL, SKOS
from rdflib.collection import Collection

from .schema import Schema
from .property import Property
from .property_types import PrimitiveType, RefType
from .typing import JsonSchema, PropertyType, RdfNodeName

logging.basicConfig(level=logging.INFO, format="%(message)s")

# we manually define this because the preinstalled namespace in rdflib doesn't include some terms we use,
# e.g. 'definition'
PROV = Namespace("http://www.w3.org/ns/prov#")
OBO_IN_OWL = Namespace("http://www.geneontology.org/formats/oboInOwl#")

PRIMITIVE_TYPES = {
    'xsd:string': 'string',
    'xsd:anyURI': 'string',
}

# properties that should appear in the json schema even if they aren't present in the ttl file
UNIVERSAL_PROPERTIES = {
    'rdfs:label': Property('rdfs:label', "A human-readable name for the entity."),
    'id': Property('id', "UUID for this entity."),
    'describedBy': Property('describedBy', "The URL reference to the JSON Schema that defines this object."),
}

SKIPPABLE_DOMAIN_PREDICATES = [
    RDF.type,     # this just indicates something is a property, which we already know
    RDFS.domain,  # no point annotating domain, since it's how we get a list of props for a class to begin with
]

SKIPPABLE_RESTRICTION_PREDICATES = [
    RDF.type,        # indicates that it's a restriction property. we check this explicitly before scanning.
    OWL.onProperty,  # we grab this beforehand as well to see what property the restrictions apply to.
]


@dataclass
class TtlSchemaGenerator:
    class_name: str
    ttl_file_path: str

    schema: Schema = field(init=False)

    def __post_init__(self) -> None:
        # parse in the graph in the ttl file
        with open(self.ttl_file_path, 'r') as ttl_file:
            self.graph = Graph().parse(ttl_file, format='turtle')

        # note down the class we're analyzing
        self.term = self.primary_namespace.term(self.class_name)

        # set up the skeleton of the schema
        self.schema = Schema(self.term)
        self.schema.properties.update(UNIVERSAL_PROPERTIES)

    @cached_property
    def primary_namespace(self) -> Namespace:
        # primary namespace for a graph is listed both under its actual namespace and under the 'empty string' namespace
        namespace_uriref = dict([namespace for namespace in self.graph.namespaces()])['']

        return Namespace(str(namespace_uriref))

    def build_schema(self) -> JsonSchema:
        self._annotate_by_class_namespace()
        self._annotate_by_domain()

        return self.schema.as_dict()

    def _annotate_by_class_namespace(self) -> None:
        for predicate, ttl_object in self.graph.predicate_objects(self.term):
            if predicate in [PROV.definition, SKOS.definition]:
                self.schema.set_description(ttl_object.value, self.namespaced_name_for_node(predicate))
            elif predicate == RDFS.label:
                self.schema.title = ttl_object.value
            elif predicate == SKOS.prefLabel:
                self.schema.skos_preflabel = ttl_object.value
            elif predicate == SKOS.altLabel:
                self.schema.skos_altlabels.append(ttl_object.value)
            elif predicate in [OBO_IN_OWL.hasExactSynonym, SKOS.exactMatch]:
                self.schema.exact_synonym.append(ttl_object.value)
            elif predicate == OWL.equivalentClass:
                if isinstance(ttl_object, rdflib.term.BNode):
                    self._annotate_blank_node(predicate, ttl_object)
                elif isinstance(ttl_object, rdflib.term.URIRef):
                    self.schema.equivalent_class.append(self.namespaced_name_for_node(ttl_object))
                else:
                    logging.warning(
                        f"Unrecognized object type for owl:equivalentClass {ttl_object} under {self.term}, skipping.")
            elif predicate == RDFS.subClassOf:
                if isinstance(ttl_object, rdflib.term.BNode):
                    self._annotate_blank_node(predicate, ttl_object)
                elif isinstance(ttl_object, rdflib.term.URIRef):
                    self.schema.subclass_of.append(self.namespaced_name_for_node(ttl_object))
                else:
                    logging.warning(
                        f"Unrecognized object type for rdfs:subClassOf {ttl_object} under {self.term}, skipping.")
            else:
                logging.warning(f"Unknown schema-level predicate {predicate} for {self.term}, skipping.")

    def type_annotation_to_property_type(self, node: rdflib.term.Identifier) -> PropertyType:
        if isinstance(node, rdflib.term.URIRef):
            namespaced_name = self.namespaced_name_for_node(node)
            if namespaced_name in PRIMITIVE_TYPES:
                return PrimitiveType(PRIMITIVE_TYPES[namespaced_name])

            return RefType(namespaced_name)

        raise ValueError(f"Unrecognized type annotation {node}")

    def _annotate_by_domain(self) -> None:
        # look up all property definitions under this class's domain
        for term_property in self.graph.subjects(RDFS.domain, self.term):
            self.ensure_property_initialized(term_property)

            property_name = self.namespaced_name_for_node(term_property)

            # grab all fields under the property definition
            for predicate, ttl_object in self.graph.predicate_objects(term_property):
                if predicate in SKIPPABLE_DOMAIN_PREDICATES:
                    continue

                if predicate == RDFS.range:
                    if isinstance(ttl_object, rdflib.term.BNode):
                        # happens in ranges occasionally
                        if self.graph.value(ttl_object, RDF.type) != RDFS.Datatype:
                            raise ValueError("Attempted to parse non-datatype BNode as type annotation")
                        for bnode_predicate, bnode_object in self.graph.predicate_objects(ttl_object):
                            if bnode_predicate == RDF.type:
                                continue

                            if bnode_predicate == OWL.oneOf:
                                # it's listing a collection of types, so we yank 'em all out
                                types_collection = Collection(self.graph, bnode_object)
                                for type_annotation in types_collection:
                                    self.schema.properties[property_name].allowed_values.append(type_annotation.value)
                            else:
                                logging.warning(f"Skipping field {bnode_predicate} in inner BNode of {property_name}")
                    # self.schema.properties[property_name].add_type(self.type_annotation_to_property_type(ttl_object))
                elif predicate == RDFS.label:
                    self.schema.properties[property_name].title = ttl_object.value
                elif predicate == RDFS.comment:
                    self.schema.properties[property_name].comment = ttl_object.value
                elif predicate == SKOS.prefLabel:
                    self.schema.properties[property_name].skos_preflabel = ttl_object.value
                elif predicate == SKOS.definition:
                    self.schema.properties[property_name].description = ttl_object.value
                elif predicate == RDFS.subPropertyOf:
                    self.schema.properties[property_name].parent_properties.append(
                        RefType(self.namespaced_name_for_node(ttl_object))
                    )
                else:
                    logging.warning(
                        f"Skipping domain-level property field {predicate} with value {ttl_object} "
                        f" for {property_name}."
                    )

    def ensure_property_initialized(self, target_property: rdflib.term.Identifier) -> None:
        property_name = target_property.n3(self.graph.namespace_manager)
        if property_name not in self.schema.properties:
            self.schema.properties[property_name] = Property(property_name, str(target_property))

    def namespaced_name_for_node(self, node: rdflib.term.Identifier) -> RdfNodeName:
        name: str = node.n3(self.graph.namespace_manager)  # hardcoding type for type annotations
        return RdfNodeName(name)

    def _annotate_blank_node(self, predicate: rdflib.term.Identifier, ttl_object: rdflib.term.Identifier) -> None:
        if self.graph.value(ttl_object, RDF.type) != OWL.Restriction:
            raise ValueError("Tried to process a blank node that isn't a restriction property.")

        # annotating a property means there's at least one additional property
        target_property = self.graph.value(ttl_object, OWL.onProperty)
        namespaced_target_name = self.namespaced_name_for_node(target_property)

        self.ensure_property_initialized(target_property)

        for predicate, ttl_object in self.graph.predicate_objects(ttl_object):
            if predicate in SKIPPABLE_RESTRICTION_PREDICATES:
                continue

            if predicate == OWL.cardinality:
                if ttl_object.value == 1:
                    self.schema.properties[namespaced_target_name].required = True
                else:
                    logging.error(
                        f"Found non-one cardinality for property {namespaced_target_name} ({ttl_object.value}), ignoring"
                    )

            elif predicate == OWL.minCardinality:
                self.schema.properties[namespaced_target_name].min_cardinality = ttl_object.value

            elif predicate == OWL.maxCardinality:
                self.schema.properties[namespaced_target_name].max_cardinality = ttl_object.value

            elif predicate == OWL.allValuesFrom:
                self.schema.properties[namespaced_target_name].add_type(
                    self.type_annotation_to_property_type(ttl_object),
                    restrictive=True,
                )

            elif predicate == OWL.someValuesFrom:
                self.schema.properties[namespaced_target_name].min_cardinality = 0
                self.schema.properties[namespaced_target_name].add_type(
                    self.type_annotation_to_property_type(ttl_object),
                    restrictive=False,
                )
            else:
                logging.warning(f"Skipping restriction property field {predicate} with value {ttl_object}.")

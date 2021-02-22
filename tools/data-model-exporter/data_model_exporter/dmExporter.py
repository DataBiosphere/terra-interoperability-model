"""!/usr/bin/env python"""

# Create a basic CLI tool that parses the arg list defined in the spec
# (as linked in the parent epic) and hands off the args to a stub driver method

import argparse
import json

from rdflib import Graph, Namespace, OWL, RDFS
# TODO: can pull this out of the local file (prefix: TerraDCAT_ap)
Terra = Namespace("http://datamodel.terra.bio/TerraDCAT_ap#")
# the builtin RDFLIB PROV NS does not define 'definition' for unknown reasons, hence this ad hoc def
Prov = Namespace("http://www.w3.org/ns/prov#")

# arguments defined in spec
# 1) a path to the data model *.TTL file
# 2) a "class file" (newline delimited list of strings that correspond to RDF classes)
def get_arguments():
    parser = argparse.ArgumentParser(description='Process data model export')
    parser.add_argument('-f', '--filePath', help="a path to the data model", required=True)
    # TODO: add required flag back in, remove default? cant get CLI list parsing working properly.
    # TODO: this will be parsed from a file later on
    parser.add_argument('-c', '--classPath', nargs='+', help="a class listing file", required=True)
    args = parser.parse_args()
    return args.filePath, args.classPath


def run(file_path, class_name):
    with open(file_path, 'r') as ttl_file:
        # TODO: confirm that this URL is valid
        rdf_term = Terra.term(class_name)
        print("rdf_term: "+rdf_term)
        # parse the file
        g = Graph()
        g.parse(ttl_file, format='turtle')
        # TODO:
        properties = {
            "describedBy": {
                "description": "The URL reference to the JSON Schema that defines this object.",
                "type": "string"
            },
            "id": {
                "description": "UUID for this entity.",
                "type": "string"
            }
        }
        # 'required' properties are those with a cardinality of exactly 1, and the hardcoded 'id' property
        # TODO verify the hardcoding of 'id'
        required = ['id','describedBy']

        ## TODO punting on rdfs:subClassOf linkage

        # pull all RDF triples with the given rdf_term as the 'subject'
        term_triples = g.triples((rdf_term, None, None))
        for triple in term_triples:
            # any OWL equivalentClass predicate is a 'property'
            if triple[1] == OWL.equivalentClass:
                # the 'object' node reached via the equivalentClass predicate is a 'blank node' in
                # RDF; this node is anonymous and serves as a container for composite property information
                container_node = triple[2]

                # required prop?
                cardinality = g.value(container_node, OWL.cardinality, None)
                prop = g.value(container_node, OWL.onProperty, None)

                # TODO fix up the logic we are using on rdfs:range vs other
                ref = prop.n3(g.namespace_manager)
                properties[prop.n3(g.namespace_manager)] = {
                    '$ref': ref,
                }

                # should limit this to exactly 1 (take the cardinality seriously)
                if cardinality and cardinality.value == 1:
                    required.append(prop.n3(g.namespace_manager))

        json_schema = {
            '$id': rdf_term,
            '$schema': "http://json-schema.org/draft-07/schema#/",
            'title': g.value(rdf_term, RDFS.label),
            # TODO: change "description" to "definition"
            'definition': str(g.value(rdf_term, Prov.definition)),
            'definitions': {},
            'type': 'object',
            'additionalProperties': True,
            'properties': properties,
            'required': required
        }

        print(json.dumps(json_schema, indent=4))

# class to implement RDF to JSON transformation
# todo: DSPDC-1537
# Per the spec linked in the parent epic, we will need to implement a method that consumes as input:
#  A list of class names (this will be parsed from a file later on, but can be hardcoded or passed via the CLI to start for testing purposes)
#  The path to the relevant TIM TTL file (again can be hardcoded or just threaded through via the CLI)
#  Execute the processing logic as defined in the spec
#  A sample spike script for how this would be approached can be found here.
def rdf_to_json(filePath, classPath):
    # todo: debugging, remove this line
    print ("RUNNING rdf_to_json()")
    print (filePath, classPath)
    #   Edge Cases:
    #   We should use RDF lib, it can easily parse TTL files and serialize to JSON schema (https://rdflib.readthedocs.io for parsing
    #   If the path to the TTL file is invalid, RDFLib will barf; we should handle this and output a useful error message
    #   This should not happen because they should be being created by a tool that creates valid TTL files.
    #   We will be punting on rdfs:subClassOf properties as there is an open question as to how we'll represent the parent classes in a json schema

    # iterate over classPath
    print("Iterating over classPath...")
    for class_name in classPath:
        # extract json for each individual class
        run(filePath, class_name)

def main():
    # get CLI arguments
    filePath, classPath = get_arguments()
    # invoke driver to transform RDF to JSON
    rdf_to_json(filePath, classPath)
    # todo:  output - write a JSON schema file
if __name__ == "__main__":
    main()

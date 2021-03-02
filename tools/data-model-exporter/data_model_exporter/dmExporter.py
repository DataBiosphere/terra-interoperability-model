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
    # TODO: two methods to input classes, CLI list vs CLI filepath argument - keep both?
    parser.add_argument('-l', '--classList', nargs='+', help="a class listing string")
    parser.add_argument('-c', '--classPath', help="a class listing file")
    args = parser.parse_args()
    # TODO: is there a nicer way to check that only one arg was provided?
    if (args.classList is None and args.classPath is None):
        print ("ERROR, you must provide a classList 'l' or classPath 'c' argument")
        exit()
    elif (args.classList and args.classPath):
        print ("ERROR, you may only provide a single classList argument")
        exit()
    elif (args.classList):
        return args.filePath, args.classList
    elif (args.classPath):
        classList = []
        classCount = 0
        with open(args.classPath, 'r') as class_file:
            while True:
                line = class_file.readline()
                if not line:
                    break
                else:
                    classCount += 1
                    classList.append(line.strip())
        print (str(classCount)+" classes parsed from "+args.classPath)
        print ("classList:  "+str(classList))
        return args.filePath, classList
    else:
        print ("Error parsing arguments, please try again...")


def run(file_path, class_name):
    with open(file_path, 'r') as ttl_file:
        rdf_term = Terra.term(class_name)
        # parse the file
        g = Graph()
        g.parse(ttl_file, format='turtle')
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
                # subject = container_node, predicate = OWL.onProperty, object)
                # TODO fix up the logic we are using on rdfs:range vs other
                ref = prop.n3(g.namespace_manager)

                # second traversal, using objects from 1st as the subject
                # processing subclasses with rdfs:range
                # have an RDFS range. We should be pulling all of the rdfs:range
                # bc if an object exists with rdfs:range, we will put it

                # pull the rdfsRangeValue directly out using Graph.value function
                # this results in nulls for dct: terms
                rdfsRangeValue = g.value(prop, RDFS.range)

                # using a try/catch for when we run into UnboundLocalError: 'rdfsRangeValue' referenced before assignment
                try:
                    properties[prop.n3(g.namespace_manager)] = {
                        'description': ref,
                        # TODO: pull the URL reference out of the graph
                        '$ref': rdfsRangeValue,
                    }
                except Exception as e:
                    raise e
                    print ("ERROR:"+str(e))
                    #exit()

                # should limit this to exactly 1 (take the cardinality seriously)
                if cardinality and cardinality.value == 1:
                    required.append(prop.n3(g.namespace_manager))

        json_schema = {
            '$id': rdf_term,
            '$schema': "http://json-schema.org/draft-07/schema#/",
            'title': g.value(rdf_term, RDFS.label),
            # json convention uses a "description" field as the definition
            'description': str(g.value(rdf_term, Prov.definition)),
            'definitions': {},
            'type': 'object',
            'additionalProperties': True,
            'properties': properties,
            'required': required
        }
        return json_schema


# class to implement RDF to JSON transformation
# todo: DSPDC-1537
# Per the spec linked in the parent epic, we will need to implement a method that consumes as input:
#  A list of class names (this will be parsed from a file later on, but can be hardcoded or passed via the CLI to start for testing purposes)
#  The path to the relevant TIM TTL file (again can be hardcoded or just threaded through via the CLI)
#  Execute the processing logic as defined in the spec
#  A sample spike script for how this would be approached can be found here.
def rdf_to_json(filePath, classList):
    #   Edge Cases:
    #   We should use RDF lib, it can easily parse TTL files and serialize to JSON schema (https://rdflib.readthedocs.io for parsing
    #   If the path to the TTL file is invalid, RDFLib will barf; we should handle this and output a useful error message
    #   This should not happen because they should be being created by a tool that creates valid TTL files.
    #   We will be punting on rdfs:subClassOf properties as there is an open question as to how we'll represent the parent classes in a json schema

    # iterate over classList
    jsonSchemaList = {}
    for class_name in classList:
        # extract json for each individual class
        jsonSchemaList[class_name] = run(filePath, class_name)
    return jsonSchemaList

def main():
    # get CLI arguments
    filePath, classList = get_arguments()
    # invoke driver to transform RDF to JSON
    jsonDict = rdf_to_json(filePath, classList)
    # write one file per class provided
    for key in jsonDict:
        outFileName = "{0}.json".format(key)
        with open(outFileName, 'w') as f:
            # TODO: print the json output to the terminal
            print(json.dumps(jsonDict[key], indent=4))
            json.dump(jsonDict[key], f)

if __name__ == "__main__":
    main()

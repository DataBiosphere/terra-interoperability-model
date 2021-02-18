__version__ = '0.1.0'
#!/usr/bin/env python

# Create a basic CLI tool that parses the arg list defined in the spec
# (as linked in the parent epic) and hands off the args to a stub driver method

import argparse

# arguments defined in spec
# 1) a path to the data model *.TTL file
# 2) a "class file" (newline delimited list of strings that correspond to RDF classes)

def get_arguments():
    parser = argparse.ArgumentParser(description='Process data model export')
    parser.add_argument('-f', '--filePath', help="a path to the data model", required=True)
    parser.add_argument('-c', '--classPath', help="a class listing file", required=True)
    args = parser.parse_args()
    return args.filePath, args.classPath

# class to implement RDF to JSON transformation
# todo: DSPDC-1537
def rdf_to_json(filePath, classPath):
    print (filePath, classPath)

def main():
    # get CLI arguments
    filePath, classPath = get_arguments()
    # invoke driver to transform RDF to JSON
    rdf_to_json(filePath, classPath)
    # todo:  output - write a JSON schema file
if __name__ == "__main__":
    main()
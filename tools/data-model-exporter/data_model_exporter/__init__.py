__version__ = '0.1.0'
#!/usr/bin/env python

# Create a basic CLI tool that parses the arg list defined in the spec
# (as linked in the parent epic) and hands off the args to a stub driver method

import argparse

# arguments defined in spec
# 1) a class listing file
# 2) a path to the data model *.TTL file we are transforming

def get_arguments(
    parser = argparse.ArgumentParser(description='Process data model export')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))
)






# output - receive a properly transformed JSON schema file.
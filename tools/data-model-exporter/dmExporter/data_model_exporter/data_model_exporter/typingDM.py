"""
type annotations and schema definitions used elsewhere in the code base live here.

if this file grows, consider splitting it up by purpose/category rather than allowing it to exceed ~100 lines
"""
from typing import Any, Literal, Protocol, TypedDict, Union

JsonSchema = dict[str, Any]

# a type annotation is either:
#  * a reference type (e.g. {"$ref": "some:thing"})
#  * a primitive type (e.g. {"type": "string"})
RefTypeConstraint = TypedDict('RefTypeConstraint', {'$ref': str})
PrimitiveTypeConstraint = TypedDict('PrimitiveTypeConstraint', {'type': str})

# a specification for a single permitted type
SingleTypeConstraint = Union[RefTypeConstraint, PrimitiveTypeConstraint]

# syntax for specifying that a property's values may have one of multiple types
MultipleTypeConstraint = TypedDict('MultipleTypeConstraint', {'oneOf': list[SingleTypeConstraint]})


# a listing of valid types for values of a property, independent of how many values it may have.
# this is also the syntax for any type restrictions on a property that may contain only a single value.
SingletonTypeConstraintExpression = Union[
    MultipleTypeConstraint,
    SingleTypeConstraint,
]


# syntax for type restrictions on a property that contains an array of values
ArrayTypeConstraintExpression = TypedDict(
    'ArrayTypeConstraintExpression',
    {
        'type': Literal['array'],
        'items': SingletonTypeConstraintExpression,
    }
)

# all possible syntaxes for expressing what data types are permitted for a property
# in our JSON schema
TypeConstraintExpression = Union[SingletonTypeConstraintExpression, ArrayTypeConstraintExpression]


# an alias for strings to explicitly say "this is the name of an RDF node"
class RdfNodeName(str):
    pass


class PropertyType(Protocol):
    @property
    def name(self) -> str: ...
    def type_constraint_dict(self) -> SingleTypeConstraint: ...

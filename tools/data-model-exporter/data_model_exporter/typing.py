from typing import Any, Literal, Protocol, TypedDict, Union

JsonSchema = dict[str, Any]

# a type annotation is either:
#  * a reference type (e.g. {"$ref": "some:thing"})
#  * a primitive type (e.g. {"type": "string"})

RefTypeEntry = TypedDict('RefTypeEntry', {'$ref': str})
PrimitiveTypeEntry = TypedDict('PrimitiveTypeEntry', {'type': str})

TypeEntry = Union[RefTypeEntry, PrimitiveTypeEntry]

MultipleTypeConstraint = TypedDict('MultipleTypeConstraint', {'oneOf': list[TypeEntry]})


# a listing of valid types for a property based on constraints,
# NOT including whether it's an array
TypeListing = Union[
    MultipleTypeConstraint,
    TypeEntry,
]


ArrayFieldTypeInformation = TypedDict(
    'ArrayFieldTypeInformation',
    {
        'type': Literal['array'],
        'items': TypeListing,
    }
)

TypeInformation = Union[TypeListing, ArrayFieldTypeInformation]


class PropertyType(Protocol):
    @property
    def name(self) -> str: ...
    def type_entry(self) -> TypeEntry: ...

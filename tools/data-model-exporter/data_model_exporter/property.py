"""
Intermediate representation for a property of a given class, including
logic to serialize to JSON schema
"""

from dataclasses import dataclass, field
import logging
from typing import Any, Literal, Optional

from data_model_exporter.common import OPTIONAL_FIELD_VALUES_TO_OMIT
from data_model_exporter.typing import ArrayTypeConstraintExpression, JsonSchema, PropertyType, RdfNodeName, \
    SingletonTypeConstraintExpression, TypeConstraintExpression
from data_model_exporter.property_types import PrimitiveType, RefType


@dataclass
class Property:
    name: str
    description: str = ""
    comment: Optional[str] = None
    title: Optional[str] = None
    skos_preflabel: Optional[str] = None
    allowed_types: list[PropertyType] = field(default_factory=list)
    allowed_values: list[str] = field(default_factory=list)
    min_cardinality: Optional[int] = None
    max_cardinality: Optional[int] = None
    required: bool = False
    parent_properties: list[RefType] = field(default_factory=list)

    # some flags for internal validation that don't end up in the json

    # set to true if a single-type constraint has been applied
    expect_no_further_type_constraints: bool = field(default=False, init=False, repr=False, compare=False)
    # determines if we already pulled in a description from another source
    description_already_set_by: Optional[RdfNodeName] = field(default=None, init=False, repr=False, compare=False)

    def set_description(self, new_description: str, source: RdfNodeName) -> None:
        if self.description_already_set_by:
            logging.warning(
                f"Setting description of property {self.name} to {new_description} (based on {source})"
                f"when it has already been defined by {self.description_already_set_by}."
            )

        self.description = new_description
        self.description_already_set_by = source

    def is_array_type(self) -> bool:
        return self.min_cardinality is not None \
            or self.max_cardinality is not None

    def add_type(self, new_type: PropertyType, restrictive: bool = False) -> None:
        if any(self.allowed_values):
            raise ValueError(
                f"Tried to add a type constraint for property {self.name}, which already has value constraints."
            )

        if self.expect_no_further_type_constraints:
            raise ValueError(
                f"Found a new type constraint ({new_type.name}) for {self.name} when a previous restrictive constraint "
                "has already been applied."
            )

        self.expect_no_further_type_constraints |= restrictive

        if new_type not in self.allowed_types:
            self.allowed_types.append(new_type)

    def add_enum_value(self, new_value: str) -> None:
        if any(self.allowed_types):
            raise ValueError(f"Tried to enumerate values for property {self.name}, which already has type constraints.")

        self.allowed_values.append(new_value)

    def base_type_info(self) -> SingletonTypeConstraintExpression:
        type_count = len(self.allowed_types)

        if type_count == 0:
            return PrimitiveType('string').type_constraint_dict()

        if type_count == 1:
            return self.allowed_types[0].type_constraint_dict()  # type: ignore

        one_of_literal: Literal['oneOf'] = 'oneOf'  # necessary for type annotations
        return {
            one_of_literal: [
                allowed_type.type_constraint_dict()
                for allowed_type in self.allowed_types
            ]
        }

    def optional_fields(self) -> dict[str, Any]:
        fields = {
            'title': self.title,
            'comment': self.comment,
            'skos:prefLabel': self.skos_preflabel,
            'minItems': self.min_cardinality,
            'maxItems': self.max_cardinality,
            'oneOf': self.allowed_values,
            'rdfs:PropertyOf': [
                parent_property.type_constraint_dict()
                for parent_property
                in self.parent_properties
            ],
        }

        return {k: v for k, v in fields.items() if v not in OPTIONAL_FIELD_VALUES_TO_OMIT}

    def type_info(self) -> TypeConstraintExpression:
        if self.is_array_type():
            base_info = ArrayTypeConstraintExpression({
                'type': 'array',
                'items': self.base_type_info()
            })

            return base_info

        return self.base_type_info()

    def as_dict(self) -> JsonSchema:
        base_info = dict(self.type_info())  # manually cast to dict to enable key assignment
        base_info.update(self.optional_fields())
        base_info['description'] = self.description

        return base_info

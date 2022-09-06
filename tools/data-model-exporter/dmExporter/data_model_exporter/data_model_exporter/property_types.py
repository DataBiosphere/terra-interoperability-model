"""
different kinds of type annotation for properties
"""
from dataclasses import dataclass

from data_model_exporter.typingDM import SingleTypeConstraint


@dataclass
class TypeAnnotation:
    name: str


class PrimitiveType(TypeAnnotation):
    def type_constraint_dict(self) -> SingleTypeConstraint:
        return {'type': self.name}


class RefType(TypeAnnotation):
    def type_constraint_dict(self) -> SingleTypeConstraint:
        return {'$ref': self.name}

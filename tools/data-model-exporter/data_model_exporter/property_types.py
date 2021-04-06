from dataclasses import dataclass

from .typing import SingleTypeConstraint


@dataclass
class TypeAnnotation:
    name: str


class PrimitiveType(TypeAnnotation):
    def type_constraint_dict(self) -> SingleTypeConstraint:
        return {'type': self.name}


class RefType(TypeAnnotation):
    def type_constraint_dict(self) -> SingleTypeConstraint:
        return {'$ref': self.name}

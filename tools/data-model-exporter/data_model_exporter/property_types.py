from dataclasses import dataclass

from .typing import TypeEntry


@dataclass
class TypeAnnotation:
    name: str


class PrimitiveType(TypeAnnotation):
    def type_entry(self) -> TypeEntry:
        return {'type': self.name}


class RefType(TypeAnnotation):
    def type_entry(self) -> TypeEntry:
        return {'$ref': self.name}

from dataclasses import dataclass, field
from typing import Any, Optional

from .property import Property
from .typing import JsonSchema


@dataclass
class Schema:
    term: str
    description: str = ""
    title: Optional[str] = None
    skos_preflabel: Optional[str] = None
    skos_altlabels: list[str] = field(default_factory=list)
    equivalent_class: list[str] = field(default_factory=list)
    subclass_of: list[str] = field(default_factory=list)
    exact_synonym: list[str] = field(default_factory=list)
    properties: dict[str, Property] = field(default_factory=dict)

    def optional_fields(self) -> dict[str, Any]:
        fields = {
            'title': self.title,
            'owl:equivalentClass': self.equivalent_class,
            'skos:exactMatch': self.exact_synonym,
            'rdfs:subClassOf': self.subclass_of,
            'skos:prefLabel': self.skos_preflabel,
            'skos:altLabel': self.skos_altlabels,
        }

        return {k: v for k, v in fields.items() if bool(v)}

    def as_dict(self) -> JsonSchema:
        base_info = {
            '$id': self.term,
            'description': self.description,
            '$schema': "http://json-schema.org/draft-07/schema#/",
            'definitions': {},
            'type': 'object',
            'additionalProperties': any(self.properties),
            'properties': {
                name: prop.as_dict()
                for name, prop
                in self.properties.items()
            },
            'required': self.required_property_names(),
            **self.optional_fields(),
        }

        return base_info

    def required_property_names(self) -> list[str]:
        return [
            prop.name
            for prop
            in self.properties.values()
            if prop.required
        ]

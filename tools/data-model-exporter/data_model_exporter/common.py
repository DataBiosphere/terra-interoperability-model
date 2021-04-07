from typing import Any


# values that mean an optional field isn't defined and should be excluded from generated schema
OPTIONAL_FIELD_VALUES_TO_OMIT: list[Any] = [
    "",
    None,
    list(),
    dict(),
    set(),
]

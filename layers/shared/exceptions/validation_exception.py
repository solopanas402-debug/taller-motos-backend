from datetime import datetime
from typing import Dict, Any, List, Type, Callable


class ValidationException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


def validate_fields(
        data: Dict[str, Any],
        schema: Dict[Type, List[str]],
        context: str = "",
        extra_validations: List[Callable[[Dict[str, Any]], None]] = None,
        field_rules: Dict[str, Dict[str, Any]] = None
):
    field_rules = field_rules or {}

    for expected_type, fields in schema.items():
        for field in fields:
            value = data.get(field, None)

            rules = field_rules.get(field, {})

            required = rules.get("required", True)
            if required and value in (None, "", [], {}):
                raise ValidationException(
                    f"El campo '{field}' {f'en {context}' if context else ''} es obligatorio y no puede estar vacío"
                )

            if value in (None, "", [], {}):
                continue

            if expected_type is datetime:
                if isinstance(value, str):
                    try:
                        datetime.fromisoformat(value)
                    except ValueError:
                        raise ValidationException(
                            f"El campo '{field}' {f'en {context}' if context else ''} debe ser una fecha válida"
                        )
                elif not isinstance(value, datetime):
                    raise ValidationException(
                        f"El campo '{field}' {f'en {context}' if context else ''} debe ser de tipo fecha"
                    )
                continue

            if not isinstance(value, expected_type):
                raise ValidationException(
                    f"El campo '{field}' {f'en {context}' if context else ''} debe ser de tipo {expected_type.__name__}"
                )

            if expected_type in (int, float):
                allow_zero = rules.get("allow_zero", False)
                if not allow_zero and value <= 0:
                    raise ValidationException(
                        f"El campo '{field}' {f'en {context}' if context else ''} debe ser mayor a 0"
                    )
                if allow_zero and value < 0:
                    raise ValidationException(
                        f"El campo '{field}' {f'en {context}' if context else ''} no puede ser negativo"
                    )

            if expected_type is str:
                if not (1 <= len(value) <= 255):
                    raise ValidationException(
                        f"El campo '{field}' {f'en {context}' if context else ''} debe tener entre 1 y 255 caracteres")

            # if expected_type is str:
            #     min_len = rules.get("min_len", 1)
            #     max_len = rules.get("max_len", 255)
            #     if not (min_len <= len(value) <= max_len):
            #         raise ValidationException(
            #             f"El campo '{field}' {f'en {context}' if context else ''} debe tener entre {min_len} y {max_len} caracteres"
            #         )

    if extra_validations:
        for validation_func in extra_validations:
            validation_func(data)

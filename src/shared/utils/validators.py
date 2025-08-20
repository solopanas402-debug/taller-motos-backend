def validate_required(field_name: str, value):
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(f"El campo '{field_name}' es obligatorio.")


def validate_quantity(field_name: str, value: float):
    if value <= 0:
        raise ValueError(f"El campo '{field_name}' debe ser mayor a 0.")


def validate_length(field_name: str, value: str, min_len: int = 1, max_len: int = 255):
    if not (min_len <= len(value) <= max_len):
        raise ValueError(f"El campo '{field_name}' debe tener entre {min_len} y {max_len} caracteres.")

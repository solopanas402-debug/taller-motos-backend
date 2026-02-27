import uuid


def generate_uuid_hex() -> str:
    """
        Genera un UUID en formato hexadecimal (32 caracteres, sin guiones)
    """
    return uuid.uuid4().hex


def generate_uuid_str() -> str:
    """
        Genera un UUID en formato estándar con guiones
    """
    return str(uuid.uuid4())


def generate_uuid_int() -> int:
    """
        Genera un UUID como número entero grande
    """
    return uuid.uuid4().int


def generate_short_numeric(digits: int = 8) -> int:
    """
    Genera un número a partir de UUID reducido a 'digits' dígitos
    """
    return uuid.uuid4().int % (10 ** digits)
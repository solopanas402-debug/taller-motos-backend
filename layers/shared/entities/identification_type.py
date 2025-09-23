from enum import Enum

class IdentificationType(str, Enum):
    CEDULA = "id_card"
    RUC = "ruc"
    PASSPORT = "passport"
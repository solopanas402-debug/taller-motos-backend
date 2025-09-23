from enum import Enum

class Gender(str, Enum):
    HOMBRE = "male"
    MUJER = "female"
    OTHER = "other"
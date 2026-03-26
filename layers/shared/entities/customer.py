class Customer:
    def __init__(self, id_customer, id_number, name, surname=None, address=None, phone=None, email=None, identification_type=None, birth_date=None, gender=None, active=True, created_at=None, updated_at=None):
        self.id_customer = id_customer
        self.id_number = id_number
        self.name = name
        self.surname = surname
        self.address = address
        self.phone = phone
        self.email = email
        self.identification_type = identification_type
        self.birth_date = birth_date
        self.gender = gender
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, row):
        return cls(
            id_customer=row.get('id_customer'),
            id_number=row.get('id_number'),
            name=row.get('name'),
            surname=row.get('surname'),
            address=row.get('address'),
            phone=row.get('phone'),
            email=row.get('email'),
            identification_type=row.get('identification_type'),
            birth_date=row.get('birth_date'),
            gender=row.get('gender'),
            active=row.get('active'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )

    def to_dict(self):
        return {
            "id_customer": self.id_customer,
            "id_number": self.id_number,
            "name": self.name,
            "surname": self.surname,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "identification_type": self.identification_type,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "active": self.active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

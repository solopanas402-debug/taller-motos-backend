class Supplier:
    def __init__(self, id_supplier, ruc, name, surname=None, address=None, phone=None, email=None, main_contact=None, active=True, created_at=None, updated_at=None):
        self.id_supplier = id_supplier
        self.ruc = ruc
        self.name = name
        self.surname = surname
        self.address = address
        self.phone = phone
        self.email = email
        self.main_contact = main_contact
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, row):
        return cls(
            id_supplier=row.get('id_supplier'),
            ruc=row.get('ruc'),
            name=row.get('name'),
            surname=row.get('surname'),
            address=row.get('address'),
            phone=row.get('phone'),
            email=row.get('email'),
            main_contact=row.get('main_contact'),
            active=row.get('active'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )

    def to_dict(self):
        return {
            "id_supplier": self.id_supplier,
            "ruc": self.ruc,
            "name": self.name,
            "surname": self.surname,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "main_contact": self.main_contact,
            "active": self.active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
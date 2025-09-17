class Mechanic:
    def __init__(self, id_mechanic, id_number, name, surname=None, phone=None, email=None, address=None, hire_date=None, salary=None, active=True, created_at=None, updated_at=None):
        self.id_mechanic = id_mechanic
        self.id_number = id_number
        self.name = name
        self.surname = surname
        self.phone = phone
        self.email = email
        self.address = address
        self.hire_date = hire_date
        self.salary = salary
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, row):
        return cls(
            id_mechanic=row.get('id_mechanic'),
            id_number=row.get('id_number'),
            name=row.get('name'),
            surname=row.get('surname'),
            phone=row.get('phone'),
            email=row.get('email'),
            address=row.get('address'),
            hire_date=row.get('hire_date'),
            salary=row.get('salary'),
            active=row.get('active'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )

    def to_dict(self):
        return {
            "id_mechanic": self.id_mechanic,
            "id_number": self.id_number,
            "name": self.name,
            "surname": self.surname,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "hire_date": self.hire_date,
            "salary": self.salary,
            "active": self.active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

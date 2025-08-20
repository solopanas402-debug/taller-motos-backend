import datetime


class Product:
    def __init__(self, id: str, code: str, name: str, description: str, price: float, stock: int, min_stock: int,
                 provider_id: str, category: str, brand: str, is_active: bool, created_at: datetime,
                 updated_at: datetime):
        self.id = id
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.min_stock = min_stock
        self.provider_id = provider_id
        self.category = category
        self.brand = brand
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, row: dict):
        return cls(id=row.get('id'), code=row.get('code'), name=row.get('name'), description=row.get('description'),
                   price=row.get('price'), stock=row.get('stock'),
                   min_stock=row.get('min_stock'), provider_id=row.get('provider_id'), category=row.get('category'),
                   brand=row.get('brand'), is_active=row.get('is_active'),
                   created_at=row.get('created_at'), updated_at=row.get('updated_at'))

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "min_stock": self.min_stock,
            "provider_id": self.provider_id,
            "category": self.category,
            "brand": self.brand,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
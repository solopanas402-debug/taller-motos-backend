import datetime


class Product:
    def __init__(self, id_product: str, code: str, name: str, description: str, price: float, stock: int,
                 min_stock: int, max_stock: int,
                 id_supplier: str, id_category: str, id_brand: str, active: bool, created_at: datetime,
                 updated_at: datetime):
        self.id_product = id_product
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.id_supplier = id_supplier
        self.id_category = id_category
        self.id_brand = id_brand
        self.active = active
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, row: dict):
        return cls(id_product=row.get('id_product'), code=row.get('code'), name=row.get('name'),
                   description=row.get('description'),
                   price=row.get('price'), stock=row.get('stock'),
                   min_stock=row.get('min_stock'), max_stock=row.get('max_stock'), id_supplier=row.get('id_supplier'),
                   id_category=row.get('id_category'),
                   id_brand=row.get('id_brand'), active=row.get('active'),
                   created_at=row.get('created_at'), updated_at=row.get('updated_at'))

    def to_dict(self):
        return {
            "id_product": self.id_product,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "min_stock": self.min_stock,
            "max_stock": self.max_stock,
            "id_supplier": self.id_supplier,
            "id_category": self.id_category,
            "id_brand": self.id_brand,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

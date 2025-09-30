from repositories.supplier_repository import SupplierRepository
import math
class SupplierUseCase:
    def __init__(self, repository : SupplierRepository):
        self.repository = repository

    def add_supplier(self, supplier):
        return self.repository.save(supplier)

    def get_suppliers(self, page=1, limit=10, search=None):
        data, total = self.repository.find_all(page, limit, search),
        totalPages = math.ceil(total / limit )  if limit > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": totalPages
            }
        }
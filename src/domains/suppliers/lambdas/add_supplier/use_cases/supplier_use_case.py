import json
from domains.suppliers.lambdas.add_supplier.repositories.supplier_repository import SupplierRepository


class SupplierUseCase:
    def __init__(self, SupplierRepository  : SupplierRepository):
        self.SupplierRepository = SupplierRepository

    def add_supplier(self, supplier):
        return self.SupplierRepository.save(supplier)

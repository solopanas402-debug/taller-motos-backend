from domains.suppliers.lambdas.delete_supplier.repositories.supplier_repository import SupplierRepository


class SupplierUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def delete_product(self, id_supplier: str):
        """
        Deletes a product from the database.
        """
        try:
            existing_supplier = self.repository.find_by_id(id_supplier)
            if existing_supplier is None:
                raise Exception(f'No se encontró el proveedor con ID {id_supplier}')

            result = self.repository.delete(id_supplier)
            return result
        except Exception as e:
            raise Exception(f'Error al eliminar el proveedor: {str(e)}')
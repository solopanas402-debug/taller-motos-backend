from domains.suppliers.lambdas.get_supplier_by_id.repositories.supplier_repository import SupplierRepository


class SupplierUseCase:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def find_supplier_by_id(self, id_supplier: str):
        """
        Busca un proveedor por ID.
        """
        try:
            result = self.repository.find_by_id(id_supplier)
            if result is None:
                raise Exception(f'No se encontró el proveedor con ID {id_supplier}')

            return result
        except Exception as e:
            raise Exception(f'Error al buscar el proveedor: {str(e)}')

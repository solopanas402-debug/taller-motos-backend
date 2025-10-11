from repositories.sale_repository import SaleRepository


class SaleUseCase:
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def delete_sale(self, id_sale: str):
        """
        Deletes a sale from the database.
        """
        try:
            existing_supplier = self.repository.find_by_id(id_sale)
            if existing_supplier is None:
                raise Exception(f'No se encontró la cotización con ID {id_sale}')

            self.repository.delete_details(id_sale)

            result = self.repository.delete(id_sale)
            return result
        except Exception as e:
            raise Exception(f'Error al eliminar la cotización: {str(e)}')

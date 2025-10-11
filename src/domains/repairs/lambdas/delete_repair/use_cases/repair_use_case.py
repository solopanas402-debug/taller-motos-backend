from repositories.repair_repository import RepairRepository


class RepairUseCase:
    def __init__(self, repository: RepairRepository):
        self.repository = repository

    def delete_repair(self, id_repair: str):
        """
        Deletes a sale from the database.
        """
        try:
            existing_supplier = self.repository.find_by_id(id_repair)
            if existing_supplier is None:
                raise Exception(f'No se encontró la cotización con ID {id_repair}')

            self.repository.delete_materials(id_repair)

            self.repository.delete_services(id_repair)

            result = self.repository.delete(id_repair)
            return result
        except Exception as e:
            raise Exception(f'Error al eliminar la cotización: {str(e)}')

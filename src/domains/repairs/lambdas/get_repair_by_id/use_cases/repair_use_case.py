from repositories.repair_repository import RepairRepository


class RepairUseCase:
    def __init__(self, repository: RepairRepository):
        self.repository = repository

    def find_repair_by_id(self, id_repair: str):
        """
        Busca una reparacion por ID.
        """
        try:
            result = self.repository.find_by_id(id_repair)
            if result is None:
                raise Exception(f'No se encontró el proveedor con ID {id_repair}')

            return result
        except Exception as e:
            raise Exception(f'Error al buscar el proveedor: {str(e)}')

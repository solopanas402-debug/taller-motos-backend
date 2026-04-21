from domains.repairs.lambdas.update_repair.repositories.repair_repository import RepairRepository


class RepairUseCase:
    def __init__(self, repository: RepairRepository):
        self.repository = repository

    def update_repair(self, id_repair: str, update_data: dict, materials: list = None):
        try:
            existing = self.repository.find_by_id(id_repair)
            if existing is None:
                raise Exception(f'No se encontró la reparación con ID {id_repair}')

            result = self.repository.update(id_repair, update_data)

            # If materials provided, replace them
            if materials is not None:
                self.repository.replace_materials(id_repair, materials)

            return result
        except Exception as e:
            raise Exception(f'Error al actualizar la reparación: {str(e)}')

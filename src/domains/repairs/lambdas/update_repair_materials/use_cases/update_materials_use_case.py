from domains.repairs.lambdas.update_repair_materials.repositories.repair_materials_repository import RepairMaterialsRepository


class UpdateMaterialsUseCase:
    def __init__(self, repository: RepairMaterialsRepository):
        self.repository = repository

    def execute(self, id_repair: str, materials: list):
        repair = self.repository.find_repair(id_repair)
        if not repair:
            raise Exception(f'No se encontró la reparación con ID {id_repair}')

        result = self.repository.replace_materials(id_repair, materials)

        return {
            "id_repair": id_repair,
            "materials_count": len(materials),
            "result": result
        }

import logging
import re

from domains.repairs.lambdas.add_repair.repositories.repair_repository import RepairRepository

logger = logging.getLogger(__name__)


class RepairUseCase:
    def __init__(self, repair_repository: RepairRepository):
        self.repair_repository = repair_repository

    def execute(self, repair_data: dict):
        print("Begin repair_use_case")
        try:
            inserted_repair = self.repair_repository.save(repair_data)
            return inserted_repair
        except Exception as e:
            logger.error(f"Error al registrar la reparacion: {e}")
            msg = str(e)
            uuid_invalid = None
            match = re.search(r'uuid: "([^"]+)"', msg)
            if match:
                uuid_invalid = match.group(1)
            if uuid_invalid:
                raise Exception(f"No se pudo insertar la reparacion: el id '{uuid_invalid}' no es un UUID válido")
            else:
                raise Exception(f"No se pudo insertar la reparacion: {msg}")

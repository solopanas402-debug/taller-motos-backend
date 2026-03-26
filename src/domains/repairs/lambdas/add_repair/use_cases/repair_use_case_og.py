import re

from domains.repairs.lambdas.add_repair.repositories.repair_repository import RepairRepository
from domains.repairs.lambdas.add_repair.repositories.vehicle_repository import VehicleRepository


class RepairUseCase:
    def __init__(self, repair_repository: RepairRepository, vehicle_repository: VehicleRepository):
        self.repair_repository = repair_repository
        self.vehicle_repository = vehicle_repository

    def add_repair(self, repair_data: dict):
        repair = repair_data["repair"]
        vehicle = repair_data["vehicle"]
        vehicle_data = None
        try:
            vehicle_data = self.vehicle_repository.find_by_id(vehicle["id_vehicle"])
            print(f"Data del vehiculo en base de datos: {vehicle_data}")
            if vehicle_data is None:
                print("Vehiculo no existe")
                vehicle_data = self.vehicle_repository.save(vehicle)
            print("Registrar Reparacion")
            response = self.repair_repository.save(repair)
            return response
        except Exception as e:
            print(f"Error al crear la reparacion: {e}")
            print(f"Data del vehiculo: {vehicle_data}")
            if vehicle_data is not None:
                self.vehicle_repository.delete_by_id(vehicle_data["id_vehicle"])
            msg = str(e)
            uuid_invalid = None
            match = re.search(r'uuid: "([^"]+)"', msg)
            if match:
                uuid_invalid = match.group(1)
            if uuid_invalid:
                raise Exception(f"No se pudo insertar la reparacion: el id '{uuid_invalid}' no es un UUID válido")
            else:
                raise Exception(f"No se pudo insertar la reparacion: {msg}")

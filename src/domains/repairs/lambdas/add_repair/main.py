import json

from db.db_client import DBClient
from exceptions.validation_exception import ValidationException
from load_initial_parameters import load_initial_parameters
from repositories.repair_repository import RepairRepository
from repositories.vehicle_repository import VehicleRepository
from use_cases.repair_use_case import RepairUseCase

db_client = DBClient.get_client()
repair_repository = RepairRepository(db_client)
vehicle_repository = VehicleRepository(db_client)
repair_use_case = RepairUseCase(repair_repository, vehicle_repository)


def lambda_handler(event, context):
    print(f'event: {event}')
    # print(f'context: {context}')
    try:
        repair_data = load_initial_parameters(event)
        # response = repair_use_case.add_repair(repair_data)
        return {
            "statusCode": 201,
            "body": json.dumps({
                "data": repair_data,
            })
        }


    except ValidationException as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e),
            })
        }

    except Exception as e:
        print(f'Error al registrar la reparacion: {e}')
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": str(e),
            })
        }

import json
from supabase import Client
from load_initial_parameters import load_initial_parameters
from repositories.mechanic_repository import MechanicRepository
from use_cases.mechanic_use_case import MechanicUseCase

db_client = Client.get_client()
repository = MechanicRepository(db_client)
use_case = MechanicUseCase(repository)

def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        mechanic = load_initial_parameters(event)
        result = use_case.add_mechanic(mechanic)
        return {
            "statusCode": 201,
            "body": json.dumps({"data": result})
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": str(e)})
        }

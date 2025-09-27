import json
from use_cases.mechanic_use_case import MechanicUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, auth_required
from repositories.mechanic_repository import MechanicRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = MechanicRepository(db_client)
use_case = MechanicUseCase(repository)

@cors_enabled  # Habilitar CORS para este endpoint
@cognito_auth_required # Asegura que el cliente esté autenticado
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Cargar parámetros del mecánico desde el evento
        mechanic = load_initial_parameters(event)

        if isinstance(mechanic, dict) and "statusCode" in mechanic:
            return mechanic  # Retornar respuesta de error si algo salió mal

        # Llamar al caso de uso para agregar el mecánico
        result = use_case.add_mechanic(mechanic)
        
        # Responder con éxito si el mecánico se agregó correctamente
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")

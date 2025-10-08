from load_initial_parameters import load_initial_parameters
from use_cases.mechanic_use_case import MechanicUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.mechanic_repository import MechanicRepository
from db.db_client import DBClient


# Inicialización de dependencias
db_client = DBClient.get_client()
repository = MechanicRepository(db_client)
use_case = MechanicUseCase(repository)


@cors_enabled  # Habilitar CORS para este endpoint
@cognito_auth_required  # Asegura que el mecánico esté autenticado
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Cargar ID del cliente desde el evento
        id_mechanic = load_initial_parameters(event)

        # Si hay error en la carga de parámetros, retornar la respuesta de error
        if isinstance(id_mechanic, dict) and "statusCode" in id_mechanic:
            return id_mechanic

        # Llamar al caso de uso para eliminar el mecánico
        result = use_case.delete_mechanic(id_mechanic)

        # Responder con éxito si el mecánico se eliminó correctamente
        return ResponseUtils.success_response({
            "message": "Mecánico eliminado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        # Manejo específico para mecánico no encontrado
        if "No se encontró el mecánico" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
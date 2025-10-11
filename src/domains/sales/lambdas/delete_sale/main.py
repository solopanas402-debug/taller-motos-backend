import json

from use_cases.sale_use_case import SaleUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.sale_repository import SaleRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = SaleRepository(db_client)
use_case = SaleUseCase(repository)


@cors_enabled  # Habilitar CORS para este endpoint
@cognito_auth_required  # Asegura que el cliente esté autenticado
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Cargar ID del proveedor desde el evento
        id_sale = load_initial_parameters(event)

        # Si hay error en la carga de parámetros, retornar la respuesta de error
        if isinstance(id_sale, dict) and "statusCode" in id_sale:
            return id_sale

        # Llamar al caso de uso para eliminar la cotización
        result = use_case.delete_sale(id_sale)

        # Responder con éxito si la cotización se eliminó correctamente
        return ResponseUtils.success_response({
            "message": "Cotización eliminado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        # Manejo específico para la cotización no encontrado
        if "No se encontró la cotización" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
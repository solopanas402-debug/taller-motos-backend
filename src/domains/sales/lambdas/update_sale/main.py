from repositories.sale_repository import SaleRepository
from use_cases.sale_use_case import SaleUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
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
        # Cargar parámetros de actualización desde el evento
        params = load_initial_parameters(event)

        # Si hay error en la carga de parámetros, retornar la respuesta de error
        if isinstance(params, dict) and "statusCode" in params:
            return params

        id_sale, update_data = params

        # Llamar al caso de uso para actualizar la cotización
        result = use_case.update_product(id_sale, update_data)

        # Responder con éxito si la cotización se actualizó correctamente
        return ResponseUtils.success_response({
            "message": "Cotización actualizado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        # Manejo específico para cotización no encontrada
        if "No se encontró el cotización" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")

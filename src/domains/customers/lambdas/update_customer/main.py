import json
from use_cases.customer_use_case import CustomerUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.customer_repository import CustomerRepository
from db.db_client import DBClient
from load_update_parameters import load_update_parameters

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = CustomerRepository(db_client)
use_case = CustomerUseCase(repository)


@cors_enabled  # Habilitar CORS para este endpoint
@cognito_auth_required  # Asegura que el cliente esté autenticado
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Cargar parámetros de actualización desde el evento
        params = load_update_parameters(event)

        # Si hay error en la carga de parámetros, retornar la respuesta de error
        if isinstance(params, dict) and "statusCode" in params:
            return params

        id_customer, update_data = params

        # Llamar al caso de uso para actualizar el cliente
        result = use_case.update_customer(id_customer, update_data)

        # Responder con éxito si el cliente se actualizó correctamente
        return ResponseUtils.success_response({
            "message": "Cliente actualizado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)
        
        # Manejo específico para cliente no encontrado
        if "No se encontró el cliente" in error_message:
            return ResponseUtils.not_found_response(error_message)
        
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
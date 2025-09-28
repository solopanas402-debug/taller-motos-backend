import json
from use_cases.customer_use_case import CustomerUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.customer_repository import CustomerRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

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

        # Cargar parámetros del cliente desde el evento
        customer = load_initial_parameters(event)

        if isinstance(customer, dict) and "statusCode" in customer:
            return customer  # Retornar respuesta de error si algo salió mal

        # Llamar al caso de uso para agregar el cliente
        result = use_case.add_customer(customer)
        
        # Responder con éxito si el cliente se agregó correctamente
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")
import json
from use_cases.product_use_cases import ProductUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.product_repository import ProductRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)

@cors_enabled  # Habilitar CORS para este endpoint
@cognito_auth_required # Asegura que el cliente esté autenticado
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:

        # Cargar parámetros del producto desde el evento
        product = load_initial_parameters(event)

        if isinstance(product, dict) and "statusCode" in product:
            return product  # Retornar respuesta de error si algo salió mal

        # Llamar al caso de uso para agregar el producto
        result = use_case.add_product(product)
        
        # Responder con éxito si el producto se agregó correctamente
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")

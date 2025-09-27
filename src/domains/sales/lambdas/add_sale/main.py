import json
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from load_initial_parameter import load_initial_parameters
from repositories.sale_detail_repository import SaleDetailRepository
from repositories.sale_repository import SaleRepository
from use_cases.sale_use_case import SaleUseCase

# Inicialización de dependencias
db_client = DBClient.get_client()
sale_repository = SaleRepository(db_client)
sale_detail_repository = SaleDetailRepository(db_client)
use_case = SaleUseCase(sale_repository, sale_detail_repository)

@cors_enabled  # Habilitar CORS para este endpoint
@cognito_auth_required # Asegura que el cliente esté autenticado
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:        

        # Cargar parámetros de la venta desde el evento
        sale_data = load_initial_parameters(event)

        if isinstance(sale_data, dict) and "statusCode" in sale_data:
            return sale_data  # Retornar respuesta de error si algo salió mal

        # Llamar al caso de uso para agregar la venta
        result = use_case.add_sale(sale_data)
        
        # Responder con éxito si la venta se agregó correctamente
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        print(f'Error al registrar la venta: {e}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")

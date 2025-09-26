import json
from use_cases.product_use_cases import ProductUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, auth_required
from decorators.role_required import role_required
from repositories.product_repository import ProductRepository
from db.db_client import DBClient

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = ProductRepository(db_client)
use_case = ProductUseCase(repository)

@cors_enabled
@auth_required
@role_required(["ADMIN", "VENDEDOR"])  # Solo estos roles pueden consultar productos
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Obtener el client_id del evento (esto proviene del token Cognito)
        client_id = event["client_id"]  # El client_id debe estar presente en el evento
        client_roles = event["client_roles"]  # Roles del cliente (verificados desde la base de datos)
        
        print(f"Cliente autenticado con ID: {client_id} y roles: {client_roles}")

        # Obtener el origen de la solicitud (por ejemplo, de un header CORS)
        origin = event.get("headers", {}).get("Origin", None)  # Obtener el origen dinámico
        headers = ResponseUtils.get_cors_headers(origin)  # Obtener los headers CORS con el origen dinámico

        parameters = event.get('queryStringParameters', None)

        if parameters is None:
            return ResponseUtils.bad_request_response("Se debe proporcionar el id del producto")

        product_id = parameters.get('id_product')
        
        if not product_id:
            return ResponseUtils.bad_request_response("El parámetro 'id_product' es obligatorio")

        print(f"Consultando producto con ID: {product_id}")
        
        # Ejecutar caso de uso
        product = use_case.get_product_by_id(product_id)

        print(f'Producto recuperado: {product}')

        if product is None:
            return ResponseUtils.not_found_response(f"No se ha encontrado producto con id: {product_id}")

        # Respuesta exitosa
        response_data = {
            "data": product,
            "client_roles": client_roles
        }
        
        return ResponseUtils.success_response(response_data, additional_headers=headers)

    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
        return ResponseUtils.bad_request_response(f"Error en los datos: {str(ve)}")
        
    except PermissionError as pe:
        print(f"Error de permisos: {str(pe)}")
        return ResponseUtils.forbidden_response(f"Sin permisos: {str(pe)}")
        
    except ConnectionError as ce:
        print(f"Error de conexión: {str(ce)}")
        return ResponseUtils.internal_server_error_response(
            "Error de conexión con la base de datos"
        )
        
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return ResponseUtils.internal_server_error_response(
            "Ha ocurrido un problema interno al consultar el producto"
        )

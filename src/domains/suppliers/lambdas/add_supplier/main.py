import json
from use_cases.supplier_use_case import SupplierUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, auth_required, role_required
from repositories.supplier_repository import SupplierRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = SupplierRepository(db_client)
use_case = SupplierUseCase(repository)

@cors_enabled  # Habilitar CORS para este endpoint
@auth_required  # Asegura que el cliente esté autenticado
@role_required(["ADMIN"])  # Solo los usuarios con rol ADMIN pueden agregar proveedores
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Obtener el client_id y roles del evento (esto proviene del token Cognito)
        client_id = event["client_id"]  # El client_id debe estar presente en el evento
        client_roles = event["client_roles"]  # Roles del cliente (verificados desde la base de datos)
        
        print(f"Cliente autenticado con ID: {client_id} y roles: {client_roles}")

        # Cargar parámetros del proveedor desde el evento
        supplier = load_initial_parameters(event)

        if isinstance(supplier, dict) and "statusCode" in supplier:
            return supplier  # Retornar respuesta de error si algo salió mal

        # Llamar al caso de uso para agregar el proveedor
        result = use_case.add_supplier(supplier)
        
        # Responder con éxito si el proveedor se agregó correctamente
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")

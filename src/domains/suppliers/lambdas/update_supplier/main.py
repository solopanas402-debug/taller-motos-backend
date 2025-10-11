from repositories.supplier_repository import SupplierRepository
from use_cases.supplier_use_case import SupplierUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = SupplierRepository(db_client)
use_case = SupplierUseCase(repository)


@cors_enabled  # Habilitar CORS para este endpoint
@cognito_auth_required  # Asegura que el proveedor esté autenticado
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Cargar parámetros de actualización desde el evento
        params = load_initial_parameters(event)

        # Si hay error en la carga de parámetros, retornar la respuesta de error
        if isinstance(params, dict) and "statusCode" in params:
            return params

        id_supplier, update_data = params

        # Llamar al caso de uso para actualizar el proveedor
        result = use_case.update_product(id_supplier, update_data)

        # Responder con éxito si el proveedor se actualizó correctamente
        return ResponseUtils.success_response({
            "message": "Proveedor actualizado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        # Manejo específico para producto no encontrado
        if "No se encontró el proveedor" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")

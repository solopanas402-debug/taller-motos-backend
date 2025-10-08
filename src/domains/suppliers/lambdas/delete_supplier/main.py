import json

from use_cases.supplier_use_case import SupplierUseCase
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from repositories.supplier_repository import SupplierRepository
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = SupplierRepository(db_client)
use_case = SupplierUseCase(repository)


@cors_enabled  # Habilitar CORS para este endpoint
@cognito_auth_required  # Asegura que el cliente esté autenticado
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Cargar ID del proveedor desde el evento
        id_supplier = load_initial_parameters(event)

        # Si hay error en la carga de parámetros, retornar la respuesta de error
        if isinstance(id_supplier, dict) and "statusCode" in id_supplier:
            return id_supplier

        # Llamar al caso de uso para eliminar el proveedor
        result = use_case.delete_product(id_supplier)

        # Responder con éxito si el proveedor se eliminó correctamente
        return ResponseUtils.success_response({
            "message": "Proveedor eliminado exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)

        # Manejo específico para proveedor no encontrado
        if "No se encontró el proveedor" in error_message:
            return ResponseUtils.not_found_response(error_message)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")
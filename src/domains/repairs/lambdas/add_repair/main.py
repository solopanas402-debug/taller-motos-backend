import json
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, auth_required, role_required
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters
from repositories.repair_repository import RepairRepository
from repositories.storage_repository import StorageRepository
from repositories.vehicle_repository import VehicleRepository
from use_cases.repair_use_case import RepairUseCase
from use_cases.save_images_use_case import SaveImagesUseCase

# Inicialización de dependencias
db_client = DBClient.get_client()
repair_repository = RepairRepository(db_client)
vehicle_repository = VehicleRepository(db_client)
repair_use_case = RepairUseCase(repair_repository)
storage_repository = StorageRepository(db_client, "repairs-images")
image_use_case = SaveImagesUseCase(storage_repository)

@cors_enabled  # Habilitar CORS para este endpoint
@auth_required  # Asegura que el cliente esté autenticado
@role_required(["ADMIN", "MECANICO"])  # Solo los usuarios con rol ADMIN o MECANICO pueden agregar reparaciones
def lambda_handler(event, context):
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Obtener el client_id y roles del evento (esto proviene del token Cognito)
        client_id = event["client_id"]  # El client_id debe estar presente en el evento
        client_roles = event["client_roles"]  # Roles del cliente (verificados desde la base de datos)
        
        print(f"Cliente autenticado con ID: {client_id} y roles: {client_roles}")

        # Cargar parámetros de la reparación desde el evento
        repair_data = load_initial_parameters(event)

        if isinstance(repair_data, dict) and "statusCode" in repair_data:
            return repair_data  # Retornar respuesta de error si algo salió mal

        # url_images = image_use_case.execute(repair_data["photos"])

        # Llamar al caso de uso para agregar la reparación
        result = repair_use_case.execute(repair_data)
        
        # Responder con éxito si la reparación se agregó correctamente
        return ResponseUtils.created_response({"data": result})

    except Exception as e:
        print(f'Error al registrar la reparación: {e}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {str(e)}")

import json
from use_cases.dashboard_use_case import DashboardUseCase
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from repositories.dashboard_repository import DashboardRepository
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = DashboardRepository(db_client)
use_case = DashboardUseCase(repository)

@cors_enabled
@debug_event
#@cognito_auth_required
def lambda_handler(event, context):
    """
    Lambda para obtener datos del dashboard
    
    Retorna:
    - total_products: Total de productos activos
    - pending_repairs: Reparaciones pendientes
    - monthly_sales: Ventas del mes actual (solo pagadas)
    - low_stock: Productos con stock bajo (< 10 unidades)
    """
    print(f'event: {event}')
    print(f'context: {context}')
    
    try:
        # Obtener datos del dashboard
        result = use_case.get_dashboard_data()
        
        return ResponseUtils.success_response({
            "message": "Datos del dashboard obtenidos correctamente",
            "data": result
        })
        
    except Exception as e:
        error_msg = str(e)
        print(f'Error al obtener datos del dashboard: {error_msg}')
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")


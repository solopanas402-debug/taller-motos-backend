import json
from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from repositories.cashbox_repository import CashboxRepository
from use_cases.cashbox_use_case import CashboxUseCase
from load_initial_parameters import load_initial_parameters

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = CashboxRepository(db_client)
use_case = CashboxUseCase(repository)

@cors_enabled
#@cognito_auth_required
def lambda_handler(event, context):
    """
    Lambda para agregar movimientos manuales a la caja chica
    
    Body esperado:
    {
        "type": "INCOME|EXPENSE|ADJUSTMENT",
        "amount": 100.50,
        "concept": "Descripción del movimiento",
        "id_user": "uuid-del-usuario"
    }
    """
    print(f'event: {event}')
    print(f'context: {context}')
    
    try:
        # Cargar y validar parámetros
        cashbox = load_initial_parameters(event)

        # Si hay error de validación, retornar
        if isinstance(cashbox, dict) and "statusCode" in cashbox:
            return cashbox

        # Registrar el movimiento
        result = use_case.add_movement(cashbox)

        return ResponseUtils.created_response({
            "message": "Movimiento registrado correctamente",
            "data": result
        })

    except Exception as e:
        error_msg = str(e)
        print(f'Error al registrar movimiento: {error_msg}')
        
        # Retornar error específico si no hay sesión abierta
        if "No hay una sesión de caja abierta" in error_msg or "No hay una caja abierta" in error_msg:
            return ResponseUtils.error_response(error_msg, 400)
        
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")

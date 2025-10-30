import json
from decorators.lambda_decorators import cors_enabled, cognito_auth_required, debug_event
from repositories.cashbox_repository import OpenCashboxRepository
from use_cases.cashbox_use_case import OpenCashboxUseCase
from db.db_client import DBClient
from utils.response_utils import ResponseUtils

# Inicialización de dependencias
db_client = DBClient.get_client()
repository = OpenCashboxRepository(db_client)
use_case = OpenCashboxUseCase(repository)


@cors_enabled
@cognito_auth_required
@debug_event
def lambda_handler(event, context):
    """
    Lambda para abrir una sesión de caja diaria

    Body esperado:
    {
        "opening_amount": 100.00,
        "opened_by": "uuid-del-usuario",
        "notes": "Opcional: notas de apertura"
    }
    """
    print(f'event: {event}')
    print(f'context: {context}')

    try:
        # Obtener y validar el body
        body = json.loads(event.get('body', '{}'))

        # Validar campos requeridos
        required_fields = ['opening_amount', 'opened_by']
        missing_fields = [field for field in required_fields if field not in body]

        if missing_fields:
            return ResponseUtils.bad_request_response(
                f"Faltan los siguientes campos requeridos: {', '.join(missing_fields)}"
            )

        # Validar que opening_amount sea un número válido
        try:
            opening_amount = float(body['opening_amount'])
        except (ValueError, TypeError):
            return ResponseUtils.bad_request_response("El campo 'opening_amount' debe ser un número válido")

        if opening_amount < 0:
            return ResponseUtils.bad_request_response("El monto de apertura no puede ser negativo")

        # Extraer datos
        opened_by = body['opened_by']
        notes = body.get('notes')

        # Ejecutar caso de uso
        result = use_case.execute(
            opening_amount=opening_amount,
            opened_by=opened_by,
            notes=notes
        )

        return ResponseUtils.created_response({
            "message": "Sesión de caja abierta correctamente",
            "data": result
        })

    except Exception as e:
        error_msg = str(e)
        print(f'Error al abrir sesión de caja: {error_msg}')

        # Retornar error específico si ya existe sesión abierta
        if "Ya existe una sesión de caja abierta" in error_msg:
            return ResponseUtils.error_response(error_msg, 400)

        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_msg}")
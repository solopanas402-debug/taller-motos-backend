from utils.response_utils import ResponseUtils
from decorators.lambda_decorators import cors_enabled, cognito_auth_required
from db.db_client import DBClient
from load_initial_parameters import load_initial_parameters
from domains.repairs.lambdas.update_repair_materials.repositories.repair_materials_repository import RepairMaterialsRepository
from domains.repairs.lambdas.update_repair_materials.use_cases.update_materials_use_case import UpdateMaterialsUseCase

db_client = DBClient.get_client()
repository = RepairMaterialsRepository(db_client)
use_case = UpdateMaterialsUseCase(repository)


@cors_enabled
@cognito_auth_required
def lambda_handler(event, context):
    print(f'event: {event}')

    try:
        params = load_initial_parameters(event)

        if isinstance(params, dict) and "statusCode" in params:
            return params

        id_repair, materials = params

        result = use_case.execute(id_repair, materials)

        return ResponseUtils.success_response({
            "message": "Materiales actualizados exitosamente",
            "data": result
        })

    except Exception as e:
        error_message = str(e)
        if "No se encontró" in error_message:
            return ResponseUtils.not_found_response(error_message)
        return ResponseUtils.internal_server_error_response(f"Error inesperado: {error_message}")

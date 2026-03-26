from domains.mechanics.lambdas.get_mechanic_by_id.repositories.mechanic_repository import MechanicRepository


class MechanicUseCase:
    def __init__(self, repository: MechanicRepository):
        self.repository = repository

    def find_customer_by_id(self, id_mechanic: str):
        """
        Busca un mecánico por ID.
        """
        try:
            result = self.repository.find_by_id(id_mechanic)
            if result is None:
                raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')

            return result
        except Exception as e:
            raise Exception(f'Error al buscar el mecánico: {str(e)}')

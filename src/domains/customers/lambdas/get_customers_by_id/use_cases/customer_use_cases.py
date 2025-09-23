from repositories.customer_repository import CustomerRepository

class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_customer_by_id(self, id: str):
        try:
            if not id:
                raise Exception(f'Se debe proporcinar el id')
            return self.repository.find_by_id(id)
        except Exception as e:
            raise Exception(f"No se pudo consultar el cliente por id {id}: {e}")

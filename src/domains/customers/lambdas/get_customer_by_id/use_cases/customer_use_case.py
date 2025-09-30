from layers.shared.entities.customer import Customer
from repositories.customer_repository import CustomerRepository


class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository
    def find_customer_by_id(self, id_customer: str):
        """
        Busca un cliente por ID.
        """
        try:
            result = self.repository.find_by_id(id_customer)
            if result is None:
                raise Exception(f'No se encontró el cliente con ID {id_customer}')
            
            return result
        except Exception as e:
            raise Exception(f'Error al buscar el cliente: {str(e)}')
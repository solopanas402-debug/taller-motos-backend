from repository.customer_repository import CustomerRepository
from src.domains.customers.entities.customer import Customer


class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def add_customer(self, customer: Customer):
        try:
            response = self.repository.save(customer)

            print(f'Respuesta de insercion de cliente: {response}')

            if len(response) == 0:
                return None

            return response[0]

        except Exception as e:
            raise Exception(f"No se pudo insertar el cliente: {e}")

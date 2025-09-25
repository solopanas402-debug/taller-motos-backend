from src.domains.customers.entities.customer import Customer
from src.domains.customers.lambdas.repository.customer_repository import CustomerRepositories


class CustomerRepository:
    def __init__(self):
        pass

    def save(self, customer: Customer):
        try:
            response = CustomerRepositories.get_customer_connection().table("customers").insert(customer.to_dict()).execute()
            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al insertar el cliente {e}')

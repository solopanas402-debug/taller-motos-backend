from src.domains.customers.lambdas.repository.customer_repository import CustomerRepositories

class CustomerRepository:
    def __init__(self):
        pass

    def find_by_id(self, id: str):
        try:
            response = CustomerRepositories.get_customer_connection().table('customers').select(
                "id_customer, id_number, name, surname, address, phone, email, identification_type, birth_date, gender, active, created_at, updated_at").eq(
                'id_number', id).single().execute()
            print(f"Respuesta de BD: {response}")
            product = response.data

            return product
        except Exception as e:
            raise Exception(f'Error al obtener los datos del cliente con id {id} {e}')

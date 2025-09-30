from supabase import Client
from layers.shared.entities.customer import Customer


class CustomerRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client
    def update(self, id_customer: str, update_data: dict):
        """
        Actualiza un cliente por ID con los datos proporcionados.
        """
        try:
            
            response = self.db_client.table("customers")\
                .update(update_data)\
                .eq('id_customer', id_customer)\
                .execute()
            
            if not response.data:
                raise Exception(f'No se encontró el cliente con ID {id_customer}')
            
            return response.data
        except Exception as e:
            print(f"Error al actualizar el cliente: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al actualizar el cliente: {str(e)}')
from supabase import Client
from layers.shared.entities.customer import Customer


class CustomerRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client
    def find_by_id(self, id_customer: str):
        """
        Busca un cliente por ID.
        """
        try:
            response = self.db_client.table("customers")\
                .select("*")\
                .eq('id_customer', id_customer)\
                .execute()
            
            if not response.data:
                return None
            
            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el cliente: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el cliente: {str(e)}')
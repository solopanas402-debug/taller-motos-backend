from supabase import Client


class CustomerRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def delete(self, id_customer: str):
        """
        Elimina un cliente por ID.
        """
        try:
            response = self.db_client.table("customers") \
                .delete() \
                .eq('id_customer', id_customer) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el cliente con ID {id_customer}')

            return response.data
        except Exception as e:
            print(f"Error al eliminar el cliente: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al eliminar el cliente: {str(e)}')

    def find_by_id(self, id_customer: str):
        """
        Busca un cliente por ID.
        """
        try:
            response = self.db_client.table("customers") \
                .select("*") \
                .eq('id_customer', id_customer) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el cliente: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el cliente: {str(e)}')

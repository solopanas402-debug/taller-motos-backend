from supabase import Client


class CustomerRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client
    def find_by_id(self, id_customer: str):
        """
        Busca un cliente por ID.
        """
        try:
            # Seleccionar columnas específicas
            response = self.db_client.table("customers")\
                .select("id_customer, name, surname, email, id_number, phone, address, city, created_at")\
                .eq('id_customer', id_customer)\
                .single()\
                .execute()
            
            return response.data
        except Exception as e:
            print(f"Error al buscar el cliente: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el cliente: {str(e)}')
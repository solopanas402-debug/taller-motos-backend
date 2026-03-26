from supabase import Client


class MechanicRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id_customer: str):
        """
        Busca un mecánico por ID.
        """
        try:
            response = self.db_client.table("mechanics") \
                .select("*") \
                .eq('id_mechanic', id_customer) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el mecánico: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el mecánico: {str(e)}')

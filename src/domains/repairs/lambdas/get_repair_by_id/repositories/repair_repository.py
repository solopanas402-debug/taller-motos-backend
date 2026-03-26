from supabase import Client


class RepairRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id_repair: str):
        """
        Busca una reparacion por ID.
        """
        try:
            response = self.db_client.table("repairs") \
                .select("*") \
                .eq('id_repair', id_repair) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar la reparación: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el reparación: {str(e)}')

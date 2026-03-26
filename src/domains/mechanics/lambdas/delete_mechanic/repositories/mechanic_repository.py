from supabase import Client


class MechanicRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def delete(self, id_mechanic: str):
        """
        Elimina un mecánico por ID.
        """
        try:
            response = self.db_client.table("mechanics") \
                .delete() \
                .eq('id_mechanic', id_mechanic) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')

            return response.data
        except Exception as e:
            print(f"Error al eliminar el mecánico: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al eliminar el mecánico: {str(e)}')

    def find_by_id(self, id_mechanic: str):
        """
        Busca un mecánico por ID.
        """
        try:
            response = self.db_client.table("mechanics") \
                .select("*") \
                .eq('id_mechanic', id_mechanic) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el mecánico: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el mecánico: {str(e)}')

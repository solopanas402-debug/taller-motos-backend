from supabase import Client


class RepairRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def delete(self, id_repair: str):
        try:
            response = self.db_client.table("repairs") \
                .delete() \
                .eq('id_repair', id_repair) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró la reparación con ID {id_repair}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al eliminar la reparación: {e}')

    def delete_materials(self, id_repair: str):
        try:
            response = self.db_client.table("repair_materials") \
                .delete() \
                .eq('id_repair', id_repair) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró detalles de la reparación con ID {id_repair}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al eliminar los detalles de la reparación: {e}')

    def delete_services(self, id_repair: str):
        try:
            response = self.db_client.table("repair_services") \
                .delete() \
                .eq('id_repair', id_repair) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró servicio de la reparación con ID {id_repair}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al eliminar los servicios de la reparación: {e}')

    def find_by_id(self, id_repair: str):
        """
        Busca una reparación por ID.
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
            raise Exception(f'Ha ocurrido un problema al buscar la reparación: {str(e)}')

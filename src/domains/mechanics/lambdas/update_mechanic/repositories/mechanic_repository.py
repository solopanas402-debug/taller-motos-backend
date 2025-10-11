from supabase import Client


class MechanicRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id: str):
        response = self.db_client.table('mechanics').select("*").eq("id_mechanic", id).maybe_single().execute()
        print(f"Respuesta de BD: {response}")

        return response.data if response else None

    def update(self, id_mechanic: str, update_data: dict):
        try:
            response = self.db_client.table("mechanics") \
                .update(update_data) \
                .eq('id_mechanic', id_mechanic) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el mecánico con ID {id_mechanic}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al actualizar el mecánico: {e}')

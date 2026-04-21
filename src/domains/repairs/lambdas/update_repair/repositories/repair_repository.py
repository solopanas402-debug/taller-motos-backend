from supabase import Client


class RepairRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id_repair: str):
        response = self.db_client.table('repairs').select("*").eq("id_repair", id_repair).limit(1).execute()
        return response.data[0] if response.data else None

    def update(self, id_repair: str, update_data: dict):
        try:
            response = self.db_client.table("repairs") \
                .update(update_data) \
                .eq('id_repair', id_repair) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró la reparación con ID {id_repair}')

            # If completing, update repair_services agreed_price with final_cost
            if update_data.get('status') == 'completed' and update_data.get('final_cost'):
                self.db_client.table("repair_services") \
                    .update({"agreed_price": update_data['final_cost']}) \
                    .eq('id_repair', id_repair) \
                    .execute()

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al actualizar la reparación: {e}')

    def replace_materials(self, id_repair: str, materials: list):
        """Delete existing materials and insert new ones"""
        try:
            # Delete existing materials for this repair
            self.db_client.table("repair_materials") \
                .delete() \
                .eq('id_repair', id_repair) \
                .execute()

            if not materials:
                return []

            # Insert new materials
            response = self.db_client.table("repair_materials") \
                .insert(materials) \
                .execute()

            return response.data if response.data else []
        except Exception as e:
            raise Exception(f'Error al actualizar materiales: {e}')

from supabase import Client


class SupplierRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id: str):
        response = self.db_client.table('suppliers').select("*").eq("id_supplier", id).maybe_single().execute()
        print(f"Respuesta de BD: {response}")

        return response.data if response else None

    def update(self, id_supplier: str, update_data: dict):
        try:
            response = self.db_client.table("suppliers") \
                .update(update_data) \
                .eq('id_supplier', id_supplier) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el proveedor con ID {id_supplier}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al actualizar el proveedor: {e}')

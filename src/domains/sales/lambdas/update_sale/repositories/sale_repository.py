from supabase import Client


class SaleRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id: str):
        response = self.db_client.table('sales').select("*").eq("id_sale", id).eq("status",
                                                                                  "quote").maybe_single().execute()
        print(f"Respuesta de BD: {response}")

        return response.data if response else None

    def update(self, id_sale: str, update_data: dict):
        try:
            response = self.db_client.table("sales") \
                .update(update_data) \
                .eq('id_sale', id_sale) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró la venta con ID {id_sale}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al actualizar la venta: {e}')

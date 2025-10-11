from supabase import Client


class SaleRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id_sale: str):
        """
        Busca una venta por ID.
        """
        try:
            response = self.db_client.table("sales") \
                .select("*") \
                .eq('id_sale', id_sale) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar la venta: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el venta: {str(e)}')

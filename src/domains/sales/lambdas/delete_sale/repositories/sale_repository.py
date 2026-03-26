from supabase import Client


class SaleRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def delete(self, id_sale: str):
        try:
            response = self.db_client.table("sales") \
                .delete() \
                .eq('id_sale', id_sale) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró la cotización con ID {id_sale}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al eliminar la cotización: {e}')

    def delete_details(self, id_sale: str):
        try:
            response = self.db_client.table("sale_details") \
                .delete() \
                .eq('id_sale', id_sale) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró detalles de la cotización con ID {id_sale}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al eliminar los detalles de la cotización: {e}')

    def find_by_id(self, id_sale: str):
        """
        Busca una cotización por ID.
        """
        try:
            response = self.db_client.table("sales") \
                .select("*") \
                .eq('id_sale', id_sale) \
                .eq('status', "quote") \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar la cotización: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar la cotización: {str(e)}')

from entities.product import Product
from supabase import Client


class ProductRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def update(self, id_product: str, update_data: dict):
        try:
            response = self.db_client.table("products")\
                .update(update_data)\
                .eq('id_product', id_product)\
                .execute()
            
            if not response.data:
                raise Exception(f'No se encontró el producto con ID {id_product}')
            
            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al actualizar el producto: {e}')

from entities.product import Product
from supabase import Client


class ProductRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def save(self, product: Product):
        try:
            response = self.db_client.table("products").insert(product).execute()
            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al insertar el producto {e}')

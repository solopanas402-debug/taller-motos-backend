from supabase import Client

from ports.product_repository import IProductRepository


class ProductRepository(IProductRepository):
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def save(self, products_data: dict) -> dict:
        response = self.db_client.rpc('bulk_insert_products', products_data).execute()
        return response.data if response.data else None

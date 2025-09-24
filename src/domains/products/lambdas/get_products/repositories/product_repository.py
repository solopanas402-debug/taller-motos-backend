from entities.product import Product
from supabase import Client


class ProductRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_all(self):
        response = self.db_client.table("products").select("*").execute()
        return response.data if response.data else []

    # def find_all(self):
    #     try:
    #         response = self.db_client.table("products").select("*").execute()
    #
    #         if not response:
    #             return None
    #
    #         products = response.data
    #
    #         print(f'productos recuperados en repository: {products}')
    #
    #         # return [Product.from_dict(row) for row in products]
    #
    #         return products
    #     except Exception as e:
    #         raise Exception(f"Error al obtener los productos: {e}")

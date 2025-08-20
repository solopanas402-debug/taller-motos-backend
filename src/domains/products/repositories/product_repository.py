from ..entities.product import Product
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

    def find_by_id(self, id: str):
        try:
            response = self.db_client.table('products').select("id, code, name, description, price, stock, min_stock,provider_id, category, brand, is_active, created_at, updated_at").eq('id', id).single().execute()
            print(f"Respuesta de BD: {response}")
            product = response.data

            return product
        except Exception as e:
            raise Exception(f'Error al obtener los datos del producto con id {id} {e}')

    def find_all(self):
        try:
            response = self.db_client.table("products").select(
                "id, code, name, description, price, stock, min_stock,provider_id, category, brand, is_active, created_at, updated_at").execute()

            if not response:
                return None

            products = response.data

            print(f'productos recuperados en repository: {products}')

            return [Product.from_dict(row) for row in products]
        except Exception as e:
            raise Exception(f"Error al obtener los productos: {e}")

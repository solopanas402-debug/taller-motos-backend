from entities.product import Product
from supabase import Client


class ProductRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id: str):
        # Seleccionar columnas específicas para reducir transferencia
        response = self.db_client.table('products').select(
            "id_product, name, code, price, stock, category_id, description, created_at"
        ).eq("id_product", id).maybe_single().execute()
        print(f"Respuesta de BD: {response}")

        return response.data if response else None

    def update(self, id_product: str, update_data: dict):
        try:
            response = self.db_client.table("products") \
                .update(update_data) \
                .eq('id_product', id_product) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el producto con ID {id_product}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al actualizar el producto: {e}')

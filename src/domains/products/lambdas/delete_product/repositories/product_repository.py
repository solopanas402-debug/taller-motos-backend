from entities.product import Product
from supabase import Client


class ProductRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client
    def delete(self, id_product: str):
        try:
            response = self.db_client.table("products")\
                .delete()\
                .eq('id_product', id_product)\
                .execute()
            
            if not response.data:
                raise Exception(f'No se encontró el producto con ID {id_product}')
            
            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al eliminar el producto: {e}')

    def find_by_id(self, id_product: str):
        """
        Busca un producto por ID.
        """
        try:
            # Seleccionar columnas específicas
            response = self.db_client.table("products") \
                .select("id_product, name, code, price, stock, category_id, description, created_at") \
                .eq('id_product', id_product) \
                .single() \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el producto: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el producto: {str(e)}')
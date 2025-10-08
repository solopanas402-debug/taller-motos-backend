from entities.product import Product
from supabase import Client


class SupplierRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def delete(self, id_product: str):
        try:
            response = self.db_client.table("suppliers") \
                .delete() \
                .eq('id_supplier', id_product) \
                .execute()

            if not response.data:
                raise Exception(f'No se encontró el proveedor con ID {id_product}')

            return response.data
        except Exception as e:
            raise Exception(f'Ha ocurrido un problema al eliminar el proveedor: {e}')

    def find_by_id(self, id_supplier: str):
        """
        Busca un proveedor por ID.
        """
        try:
            response = self.db_client.table("suppliers") \
                .select("*") \
                .eq('id_supplier', id_supplier) \
                .execute()

            if not response.data:
                return None

            return response.data[0]
        except Exception as e:
            print(f"Error al buscar el proveedor: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el proveedor: {str(e)}')
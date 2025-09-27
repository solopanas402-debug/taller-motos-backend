

class ProductRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_by_id(self, id: str):
        response = self.db_client.table('products').select("*").eq("id_product", id).maybe_single().execute()
        print(f"Respuesta de BD: {response}")

        return response.data if response else None

    # def find_by_id(self, id: str):
    #     try:
    #         response = self.db_client.table('products').select(
    #             "id_product, code, name, description, price, stock, min_stock, max_stock, id_supplier, id_category, id_brand, model, qr_url, active, created_at, updated_at").eq(
    #             'id_product', id).maybe_single().execute()
    #         print(f"Respuesta de BD: {response}")
    #         product = response.data
    #
    #         return product
    #     except Exception as e:
    #         raise Exception(f'Error al obtener los datos del producto con id {id} {e}')

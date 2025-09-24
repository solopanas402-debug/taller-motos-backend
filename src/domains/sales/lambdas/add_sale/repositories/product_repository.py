from supabase import Client


class ProductRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def update_stock(self, id_product: int, stock: int):
        print(f"Updating stock id_product:{id_product} stock:{stock}")
        self.db_client.table("products").update({"stock": stock}).eq("id_product", id_product).execute()

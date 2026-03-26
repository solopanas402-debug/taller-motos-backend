from supabase import Client


class SaleRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def save(self, sale: dict) -> dict:
        response = self.db_client.table("sales").insert(sale).execute()
        if not response.data:
            raise ValueError("No se pudo insertar la venta")
        return response.data[0]

    def delete(self, sale_id: int):
        self.db_client.table("sales").delete().eq("id_sale", sale_id).execute()

from supabase import Client


class SaleDetailRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def save(self, sale_detail: dict) -> dict:
        response = self.db_client.table("sale_details").insert(sale_detail).execute()
        if not response.data:
            raise ValueError("No se pudo insertar el detalle de la venta")
        return response.data[0]

    def delete(self, sale_id: int):
        self.db_client.table("sale_details").delete().eq("id_sale", sale_id).execute()

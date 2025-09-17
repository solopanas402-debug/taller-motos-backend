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

    # def save(self, sale_data: dict):
    #     try:
    #         sale = sale_data['sale']
    #         sale_detail = sale_data['sail_detail']
    #         response = self.db_client.table("sales").insert(sale).execute()
    #         print(f"Respuesta de insercion en sail: {response}")
    #         if (response.data is not None):
    #             response_sail_detail = self.save_sail_detail(sale_detail)
    #             if response_sail_detail is None:
    #                 raise Exception("No se pudo insertar el detalle de la venta")
    #         return response.data
    #     except Exception as e:
    #         raise Exception(f"Ha ocurrido un problema al insertar la venta: {e}")
    #
    # def save_sail_detail(self, sail_detail: dict):
    #     try:
    #         response = self.db_client.table("sail_details").insert(sail_detail).execute()
    #         return response.data
    #     except Exception as e:
    #         raise Exception(f"No se pudo insertar el detalle de la venta: {e}")

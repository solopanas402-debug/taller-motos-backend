from supabase import Client


class SellerRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def get(self, id_seller):
        response = self.db_client.table("users").get(id_seller).execute()
        if not response.data:
            raise ValueError(f"No se ha encontrado el vendedor con id: {id_seller}")

        return response.data[0]

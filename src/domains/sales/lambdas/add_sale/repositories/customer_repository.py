from supabase import Client


class CustomerRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def get(self, id_customer):
        response = self.db_client.table("customers").get(id_customer).execute()
        if not response.data:
            raise ValueError(f"No se ha encontrado el cliente con id: {id_customer}")

        return response.data[0]

from supabase import Client


class RepairRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def save(self, repair: dict):
        response = self.db_client.table("repairs").insert(repair).execute()
        return response.data[0] if response else None

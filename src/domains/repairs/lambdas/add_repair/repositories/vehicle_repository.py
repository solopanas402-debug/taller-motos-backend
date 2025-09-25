from supabase import Client


class VehicleRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def save(self, vehicle: dict):
        response = self.db_client.table("vehicles").insert(vehicle).execute()
        print(f"Insert vehicle {response}")
        return response.data[0] if response else None

    def find_by_id(self, id_vehicle: str):
        response = self.db_client.table("vehicles").select("*").eq("id_vehicle", id_vehicle).maybe_single().execute()
        return response.data if response else None

    def delete_by_id(self, id_vehicle: str):
        self.db_client.table("vehicles").delete().eq("id_vehicle", id_vehicle).execute()

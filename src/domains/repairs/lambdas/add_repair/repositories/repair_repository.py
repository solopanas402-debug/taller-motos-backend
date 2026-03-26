from supabase import Client


class RepairRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def save(self, repair_data: dict):
        print(f'Data de reparacion para guardar: {repair_data}')
        response = self.db_client.rpc(
            "insert_repair_transaction",
            {
                "vehicle_data": repair_data["vehicle"],
                "repair_data": repair_data["repair"],
                "repair_materials_data": repair_data["materials"],
                "repair_service_data": repair_data["labor"]
            }
        ).execute()

        return response.data if response.data else None

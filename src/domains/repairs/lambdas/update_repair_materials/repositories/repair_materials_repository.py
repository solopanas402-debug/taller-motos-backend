from supabase import Client


class RepairMaterialsRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_repair(self, id_repair: str):
        response = self.db_client.table('repairs') \
            .select("id_repair, status") \
            .eq("id_repair", id_repair) \
            .limit(1) \
            .execute()
        return response.data[0] if response.data else None

    def replace_materials(self, id_repair: str, materials: list):
        """Use Supabase RPC to replace materials and handle stock atomically"""
        import json
        response = self.db_client.rpc(
            "update_repair_materials_transaction",
            {
                "p_id_repair": id_repair,
                "p_materials": materials  # jsonb
            }
        ).execute()

        return response.data if response.data else {}

from supabase import create_client, Client
from src.config.config import Config

class DBClient:
    @staticmethod
    def get_client() -> Client:
        url = Config.DB_URL
        key = Config.DB_KEY
        if not url or not key:
            raise ValueError("❌ DB_URL o DB_KEY no están definidos en .env")
        return create_client(url, key)

# class DBClient:
#     @staticmethod
#     def get_client() -> "SupabaseClient":
#         return SupabaseClient()
#
#
# class SupabaseClient:
#     def __init__(self):
#         url = Config.DB_URL
#         key = Config.DB_KEY
#
#         if not url or not key:
#             raise ValueError("❌ DB_URL o DB_KEY no están definidos en .env")
#
#         self.client = create_client(url, key)
#
#     def table(self, table_name):
#         return self.client.table(table_name)
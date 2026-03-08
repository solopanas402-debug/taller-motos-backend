import os
from supabase import create_client, Client
from config.config import Config


class DBClient:
    @staticmethod
    def get_client() -> Client:
        url = Config.DB_URL or os.getenv("DB_URL")
        key = Config.DB_KEY or os.getenv("DB_KEY")
        if not url or not key:
            raise ValueError(
                "❌ DB_URL o DB_KEY no están definidos. "
                "En Lambda local usa --env-vars locals.json con DB_URL y DB_KEY."
            )
        return create_client(url, key)


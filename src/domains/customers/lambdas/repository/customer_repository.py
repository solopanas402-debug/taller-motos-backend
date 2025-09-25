from db.db_client import DBClient
from supabase import Client

class CustomerRepositories:
    def __init__(self):
        pass

    @staticmethod
    def get_customer_connection() -> Client:
        return DBClient().get_client()
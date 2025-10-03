from typing import List, Tuple
from entities.mechanic import Mechanic

class MechanicRepository:
    def __init__(self, db_client):
        self.db_client = db_client
     
    def save(self, mechanic: Mechanic):
        data = mechanic.to_dict()
        response = self.db_client.table("mechanics").insert(data).execute()
        return response.data
     
    def find_all(self, page: int = 1, limit: int = 10, search: str = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("mechanics").select("*", count="exact")
        
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"surname.ilike.{search_pattern},"
                f"email.ilike.{search_pattern}"
            )
        response = query.range(offset, offset + limit - 1).execute()
        return response.data, response.count
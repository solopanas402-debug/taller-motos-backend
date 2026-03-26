from typing import Tuple
from entities.brand import Brand

class BrandRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 1000, type_brand: str = None) -> Tuple[list[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("brands").select("*", count="exact")
        if type_brand:
            query = query.eq('type_brand', type_brand)
        response = query.limit(limit).offset(offset).execute()
        return (response.data or [], response.count or 0)

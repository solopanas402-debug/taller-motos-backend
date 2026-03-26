from typing import Tuple
from entities.category import Category

class CategoryRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 1000) -> Tuple[list[dict], int]:
        offset = (page - 1) * limit
        response = self.db_client.table("categories").select("*", count="exact").limit(limit).offset(offset).execute()
        return (response.data or [], response.count or 0)

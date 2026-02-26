from typing import Tuple, List


class BrandRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str = None, type_brand:str = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        query = self.db_client.table("brands").select("*", count="exact")

        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                # f"description.ilike.{search_pattern},"
            )

        if type_brand:
            query = query.eq("type_brand", type_brand)

        response = query.range(offset, offset + limit - 1).execute()
        return response.data, response.count

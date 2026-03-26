from typing import Tuple

from entities.product import Product


class ProductRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None) -> Tuple[list[dict], int]:
        offset = (page - 1) * limit
        
        # Construir query base
        query = self.db_client.table("products").select("*")
        
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"description.ilike.{search_pattern},"
                f"code.ilike.{search_pattern}"
            )
        
        # Ejecutar query con paginación usando limit y offset
        response = query.limit(limit).offset(offset).execute()
        
        # Obtener el total de registros con una query separada
        count_query = self.db_client.table("products").select("*", count="exact")
        if search:
            search_pattern = f"%{search}%"
            count_query = count_query.or_(
                f"name.ilike.{search_pattern},"
                f"description.ilike.{search_pattern},"
                f"code.ilike.{search_pattern}"
            )
        
        count_response = count_query.execute()
        total = count_response.count if hasattr(count_response, 'count') else len(response.data or [])
        
        return (response.data or [], total)


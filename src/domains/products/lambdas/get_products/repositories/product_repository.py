from typing import Tuple

from entities.product import Product


class ProductRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None) -> Tuple[list[dict], int]:
        offset = (page - 1) * limit
        
        # Seleccionar columnas específicas para reducir ancho de banda
        query = self.db_client.table("products").select(
            "id_product, name, code, price, stock, category_id, description, created_at",
            count="exact"
        )
        
        if search:
            # Buscar primero en campos indexados (name y code)
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"code.ilike.{search_pattern}"
            )
        
        # Una sola query con count en el mismo llamado
        response = query.limit(limit).offset(offset).execute()
        total = response.count if hasattr(response, 'count') else 0
        
        return (response.data or [], total)


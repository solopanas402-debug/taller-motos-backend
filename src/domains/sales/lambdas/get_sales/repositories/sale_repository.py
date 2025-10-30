from typing import List, Tuple, Any


class SaleRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None, record_type: str | None = None) -> \
            tuple[list[Any] | Any, int | Any] | None:
        offset = (page - 1) * limit

        response = self.db_client.rpc("get_sales_cpr", {
            "p_id_sale": None,
            "p_search": search,
            "p_limit": limit,
            "p_offset": offset,
            "p_record_type": record_type
        }).execute()

        data = response.data.get("data", [])
        total = response.data.get("total", 0)

        return data, total

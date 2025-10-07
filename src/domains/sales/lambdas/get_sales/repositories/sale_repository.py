from typing import List, Tuple


class SaleRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None, record_type: str | None = None) -> \
            Tuple[
                List[dict], int]:
        offset = (page - 1) * limit

        select_str = "id_sale,invoice_number,subtotal,tax,total,sale_date,created_at,customer:customers(name,surname)"
        query = (
            self.db_client
            .table("sales")
            .select(select_str, count="exact")
            .order("sale_date", desc=True)
        )

        if record_type == "quote":
            query = query.eq("status", "quote")
        elif record_type == "sale":
            query = query.neq("status", "quote")

        if search:
            query = query.or_(
                f"customer.name.ilike.%{search}%,customer.surname.ilike.%{search}%"
            )

        response = query.range(offset, offset + limit - 1).execute()
        return response.data or [], response.count or 0

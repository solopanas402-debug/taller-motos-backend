from typing import List
from src.domains.customers.lambdas.repository.customer_repository import CustomerRepositories


class CustomerRepository:
    def __init__(self):
        pass

    def find_all(self, page: int = 1, limit: int = 10, search: str = None) -> List[dict]:
        offset = (page - 1) * limit
        query = CustomerRepositories.get_customer_connection().table("customers").select("*", count="exact")

        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"surname.ilike.{search_pattern},"
                f"email.ilike.{search_pattern}"
            )
        response = query.range(offset, offset + limit - 1).execute()
        return response.data, response.count
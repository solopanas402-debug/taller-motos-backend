
from repositories.customer_repository import CustomerRepository
import math
class CustomerUseCase:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def add_customer(self, customer):
        return self.repository.save(customer)

    def get_customers(self, page=1, limit=10, search=None):
        data, total = self.repository.find_all(page, limit, search)
        totalPages = math.ceil(total / limit )  if limit > 0 else 0

        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": totalPages
            }
        }

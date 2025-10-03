
import math

from src.domains.sales.lambdas.get_sale.repositories.sale_repository import SaleRepository


class SaleUseCase:
    def __init__(self, repository : SaleRepository):
        self.repository = repository

    def get_sales(self, page=1, limit=10, search=None):
        data, total = self.repository.find_all(page, limit, search)
        totalPages = math.ceil(total / limit )  if limit > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": totalPages
            },
        }



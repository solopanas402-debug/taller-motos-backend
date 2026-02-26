import math

from repositories.brand_repository import BrandRepository


class BrandUseCase:
    def __init__(self, repository: BrandRepository):
        self.repository = repository

    def get_customers(self, page=1, limit=10, search=None, type_brand=None):
        data, total = self.repository.find_all(page, limit, search, type_brand)
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
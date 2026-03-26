import math

from domains.categories.lambdas.get_categories.repositories.category_repository import CategoryRepository


class CategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

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
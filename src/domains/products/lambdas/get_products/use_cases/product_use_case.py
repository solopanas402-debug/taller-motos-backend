from entities.product import Product
from repositories.product_repository import ProductRepository


class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_all_products(self, page=1, limit=10, search=None):
        data, total = self.repository.find_all(page, limit, search)
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
            },
        }

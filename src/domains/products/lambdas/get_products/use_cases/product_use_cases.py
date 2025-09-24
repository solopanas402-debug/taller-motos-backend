from entities.product import Product
from repositories.product_repository import ProductRepository


class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_all_products(self):
        response = self.repository.find_all()

        if len(response) == 0:
            return []

        return response

from repositories.product_repository import ProductRepository


class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_product_by_id(self, id: str):
        response = self.repository.find_by_id(id)
        return response

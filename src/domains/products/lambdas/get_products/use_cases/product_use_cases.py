from entities.product import Product
from repositories.product_repository import ProductRepository


class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_all_products(self):
        try:
            products = self.repository.find_all()

            if len(products) == 0:
                return []

            # products_dict = [product.to_dict() for product in products]
            return products
        except Exception as e:
            raise Exception(f"No se pudo consultar los productos: {e}")

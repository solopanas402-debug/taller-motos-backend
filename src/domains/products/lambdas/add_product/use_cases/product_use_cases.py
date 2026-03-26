from entities.product import Product
from domains.products.lambdas.add_product.repositories.product_repository import ProductRepository


class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def add_product(self, product: Product):
        try:
            response = self.repository.save(product)

            print(f'Respuesta de insercion de producto: {response}')

            if len(response) == 0:
                return None

            return response[0]

        except Exception as e:
            raise Exception(f"No se pudo insertar el producto: {e}")

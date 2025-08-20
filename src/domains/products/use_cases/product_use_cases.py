from ..entities.product import Product
from ..repositories.product_repository import ProductRepository


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

    def get_all_products(self):
        try:
            products = self.repository.find_all()

            if len(products) == 0:
                return []

            products_dict = [product.to_dict() for product in products]
            return products_dict
        except Exception as e:
            raise Exception(f"No se pudo consultar los productos: {e}")

    def get_product_by_id(self, id: str):
        try:
            if not id:
                raise Exception(f'Se debe proporcinar el id')
            return self.repository.find_by_id(id)
        except Exception as e:
            raise Exception(f"No se pudo consultar el producto por id {id}: {e}")

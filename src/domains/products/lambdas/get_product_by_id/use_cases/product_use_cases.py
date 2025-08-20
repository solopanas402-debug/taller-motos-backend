from repositories.product_repository import ProductRepository


class ProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_product_by_id(self, id: str):
        try:
            if not id:
                raise Exception(f'Se debe proporcinar el id')
            return self.repository.find_by_id(id)
        except Exception as e:
            raise Exception(f"No se pudo consultar el producto por id {id}: {e}")

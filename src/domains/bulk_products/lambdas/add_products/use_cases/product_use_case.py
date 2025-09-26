import logging
import re

from ports.product_repository import IProductRepository

logger = logging.getLogger(__name__)


class ProductUseCase:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def execute(self, products_data: dict):
        logger.info("Begin product_use_case")
        try:
            inserted_products = self.product_repository.save(products_data)
            return inserted_products
        except Exception as e:
            logger.error(f"Error al registrar la reparacion: {e}")
            msg = str(e)
            uuid_invalid = None
            match = re.search(r'uuid: "([^"]+)"', msg)
            if match:
                uuid_invalid = match.group(1)
            if uuid_invalid:
                raise Exception(f"No se pudo insertar la reparacion: el id '{uuid_invalid}' no es un UUID válido")
            else:
                raise Exception(f"No se pudo insertar la reparacion: {msg}")

from abc import ABC, abstractmethod


class IProductRepository(ABC):
    @abstractmethod
    def save(self, products_data: dict) -> dict:
        """ Save product data array """
        pass

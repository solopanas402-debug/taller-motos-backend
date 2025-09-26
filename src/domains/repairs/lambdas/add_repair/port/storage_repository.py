from abc import ABC, abstractmethod
from typing import List


class IStorageRepository(ABC):
    @abstractmethod
    def upload_photos(self, folder: str, photos: list) -> List[str]:
        """ Upload photos and return urls """
        pass

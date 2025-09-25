from typing import List

from repositories.storage_repository import StorageRepository


class SaveImagesUseCase:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    def execute(self, photos: list) -> List[str]:
        print("Begin save_image_usecase")
        try:
            urls = self.storage_repository.upload_photos("", photos)
            return urls
        except Exception as e:
            raise Exception(f"Error al registrar las imagenes: {e}")

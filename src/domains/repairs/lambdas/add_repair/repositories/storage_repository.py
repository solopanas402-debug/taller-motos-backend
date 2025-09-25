from supabase import Client
import mimetypes


class StorageRepository:
    def __init__(self, db_client: Client, bucket: str):
        self.db_client = db_client
        self.bucket = bucket

    def upload_photos(self, folder: str, photos: list) -> list[str]:
        urls = []
        for photo in photos:
            path = f'{folder}/{photo["filename"]}'

            # Inferir MIME type desde el nombre del archivo
            mime_type, _ = mimetypes.guess_type(photo["filename"])
            if not mime_type:
                mime_type = "application/octet-stream"  # fallback

            # Eliminar si existe
            # try:
            #     self.db_client.storage.from_(self.bucket).remove([path])
            # except Exception:
            #     pass

            # Subir con content_type
            self.db_client.storage.from_(self.bucket).upload(
                path,
                photo["content"],
                {"content-type": mime_type}  # aquí es clave
            )

            urls.append(self.db_client.storage.from_(self.bucket).get_public_url(path))

        return urls

from repositories.seller_repository import SellerRepository


class SellerUseCase:
    def __init__(self, seller_repository: SellerRepository):
        self.seller_repository = seller_repository

    def is_seller_exists(self, id_seller):
        print("Begin is_seller_exists")
        result = True
        try:
            customer = self.seller_repository.get(id_seller)
            if not customer:
                result = False
        except Exception as e:
            print(f"Ha ocurrido un problema en seller_use_case: {e}")
            result = False

        return result

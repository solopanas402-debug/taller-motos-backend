import re

from repositories.sale_detail_repository import SaleDetailRepository
from repositories.sale_repository import SaleRepository


class SaleUseCase:
    def __init__(self, sale_repository: SaleRepository, sale_detail_repository: SaleDetailRepository):
        self.sale_repository = sale_repository
        self.sale_detail_repository = sale_detail_repository

    def add_sale(self, sale_data: dict):
        print(f'Begin add_sale')
        inserted_sale = None
        try:
            print(f'sale_data: {sale_data}')
            sale = sale_data["sale"]
            details = sale_data["details"]

            inserted_sale = self.sale_repository.save(sale)

            inserted_details = []
            for detail_item in details:
                # detail_item["id_sale"] = inserted_sale["id_sale"]
                inserted_detail = self.sale_detail_repository.save(detail_item)
                inserted_details.append(inserted_detail)

            return {
                "sale": inserted_sale,
                "detail": inserted_details
            }

        except Exception as e:
            if inserted_sale:
                self.sale_detail_repository.delete(inserted_sale["id_sale"])
                self.sale_repository.delete(inserted_sale["id_sale"])
            msg = str(e)
            uuid_invalid = None
            match = re.search(r'uuid: "([^"]+)"', msg)
            if match:
                uuid_invalid = match.group(1)

            if uuid_invalid:
                raise Exception(f"No se pudo insertar la venta: el id '{uuid_invalid}' no es un UUID válido")
            else:
                raise Exception(f"No se pudo insertar la venta: {msg}")

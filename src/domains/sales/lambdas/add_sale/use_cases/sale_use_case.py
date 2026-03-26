import re
import logging
from typing import Optional

from domains.sales.lambdas.add_sale.repositories.product_repository import ProductRepository
from domains.sales.lambdas.add_sale.repositories.sale_detail_repository import SaleDetailRepository
from domains.sales.lambdas.add_sale.repositories.sale_repository import SaleRepository

logger = logging.getLogger(__name__)


class SaleUseCase:
    def __init__(self, sale_repository: SaleRepository,
                 sale_detail_repository: SaleDetailRepository,
                 ):
        self.sale_repository = sale_repository
        self.sale_detail_repository = sale_detail_repository

    def add_sale(self, sale_data: dict) -> dict:
        logger.info("Begin add_sale")
        logger.debug(f"sale_data: {sale_data}")


        try:
            inserted_result = self.sale_repository.save(sale_data)

            # Si la inserción fue exitosa y tenemos un ID de venta
            if inserted_result and isinstance(inserted_result, dict) and "id_sale" in inserted_result:
                id_sale = inserted_result["id_sale"]
                logger.info(f"Venta insertada con ID: {id_sale}. Obteniendo detalle completo para la respuesta...")

                full_sale = self.sale_repository.get_full_by_id(id_sale)
                if full_sale:
                    # Formatear la respuesta exactamente según lo solicitado por el usuario
                    customer_data = full_sale.get("customer", {})
                    fullname = f"{customer_data.get('name', '')} {customer_data.get('surname', '')}".strip()

                    formatted_sale = {
                        "id_sale": full_sale.get("id_sale"),
                        "invoice_number": full_sale.get("invoice_number"),
                        "subtotal": full_sale.get("subtotal"),
                        "tax": full_sale.get("tax"),
                        "total_discount": full_sale.get("total_discount", 0.0),
                        "status": full_sale.get("status"),
                        "sale_date": full_sale.get("created_at"),
                        "customer": {
                            "id_customer": customer_data.get("id_customer"),
                            "fullname": fullname,
                            "email": customer_data.get("email"),
                            "id_number": customer_data.get("id_number")
                        },
                        "details": []
                    }

                    for detail in full_sale.get("details", []):
                        formatted_sale["details"].append({
                            "product": detail.get("product"),
                            "quantity": detail.get("quantity"),
                            "discount": detail.get("discount", 0.0),
                            "subtotal": detail.get("subtotal")
                        })

                    return formatted_sale

            return inserted_result



        except Exception as e:
            logger.error(f"Error al registrar la venta: {e}")
            msg = str(e)
            uuid_invalid = self._extract_invalid_uuid(msg)
            if uuid_invalid:
                raise Exception(f"No se pudo insertar la venta: el id '{uuid_invalid}' no es un UUID válido")
            raise Exception(f"No se pudo insertar la venta: {msg}")


    @staticmethod
    def _extract_invalid_uuid(msg: str) -> Optional[str]:
        """Extrae el UUID inválido de un mensaje de error si existe"""
        match = re.search(r'uuid: "([^"]+)"', msg)
        return match.group(1) if match else None

import logging
from typing import List, Tuple, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SaleRepository:
    def __init__(self, db_client):
        self.db_client = db_client
        logger.info('SaleRepository initialized')

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None, record_type: str | None = None, payment_method: str | None = None) -> \
            tuple[list[Any] | Any, int | Any] | None:
        logger.info(f'=== SaleRepository.find_all CALLED ===')
        logger.info(f'Input parameters: page={page}, limit={limit}, search={search}, record_type={record_type}, payment_method={payment_method}')
        
        try:
            offset = (page - 1) * limit
            logger.info(f'Calculated offset: {offset}')

            # Optimizado: pasar solo parámetros necesarios al RPC
            rpc_params = {
                "p_id_sale": None,
                "p_search": search if search else None,
                "p_limit": limit,
                "p_offset": offset,
                "p_record_type": record_type if record_type else None,
                "p_payment_method": payment_method if payment_method else None
            }
            logger.info(f'RPC parameters: {rpc_params}')
            logger.info(f'Calling RPC: get_sales_cpr')
            
            response = self.db_client.rpc("get_sales_cpr", rpc_params).execute()
            logger.info(f'RPC response received. Response type: {type(response)}')
            
            if response and response.data:
                logger.info(f'Response data type: {type(response.data)}')
                logger.info(f'Response data: {response.data}')
                
                # response.data es el resultado del RPC (un dict o lista)
                if isinstance(response.data, dict):
                    data = response.data.get("data", [])
                    total = response.data.get("total", 0)
                elif isinstance(response.data, list):
                    # Si el RPC devuelve directamente una lista
                    data = response.data
                    total = len(data)
                else:
                    data = []
                    total = 0
                
                logger.info(f'Extracted from response: data items={len(data)}, total={total}')
                logger.info(f'=== SaleRepository.find_all COMPLETED SUCCESSFULLY ===')
                return data, total
            else:
                logger.warning('RPC response is None or has no data')
                return [], 0
        
        except Exception as e:
            logger.error(f'ERROR in SaleRepository.find_all: {type(e).__name__}: {str(e)}', exc_info=True)
            raise

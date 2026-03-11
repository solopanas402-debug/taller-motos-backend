import logging
from typing import List, Tuple, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class QuotationRepository:
    def __init__(self, db_client):
        self.db_client = db_client
        logger.info('QuotationRepository initialized')

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None, record_type: str | None = "quotation", payment_method: str | None = None) -> \
            tuple[list[Any] | Any, int | Any] | None:
        logger.info(f'=== QuotationRepository.find_all CALLED ===')
        logger.info(f'Input parameters: page={page}, limit={limit}, search={search}, record_type={record_type}, payment_method={payment_method}')
        
        try:
            offset = (page - 1) * limit
            logger.info(f'Calculated offset: {offset}')

            rpc_params = {
                "p_id_sale": None,
                "p_search": search,
                "p_limit": limit,
                "p_offset": offset,
                "p_record_type": record_type,
                "p_payment_method": payment_method
            }
            logger.info(f'RPC parameters: {rpc_params}')
            logger.info(f'Calling RPC: get_sales_cpr')
            
            response = self.db_client.rpc("get_sales_cpr", rpc_params).execute()
            logger.info(f'RPC response received. Response type: {type(response)}, Response data type: {type(response.data)}')
            logger.info(f'Response data: {response.data}')

            data = response.data.get("data", [])
            total = response.data.get("total", 0)
            logger.info(f'Extracted from response: data items={len(data)}, total={total}')
            logger.info(f'=== QuotationRepository.find_all COMPLETED SUCCESSFULLY ===')

            return data, total
        
        except Exception as e:
            logger.error(f'ERROR in QuotationRepository.find_all: {type(e).__name__}: {str(e)}', exc_info=True)
            raise

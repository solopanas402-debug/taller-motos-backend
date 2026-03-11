import math
import logging

from repositories.quotation_repository import QuotationRepository

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class QuotationUseCase:
    def __init__(self, repository: QuotationRepository):
        self.repository = repository
        logger.info('QuotationUseCase initialized')

    def get_quotations(self, page=1, limit=10, search=None, record_type="quotation", payment_method=None):
        logger.info(f'=== QuotationUseCase.get_quotations CALLED ===')
        logger.info(f'Input parameters: page={page}, limit={limit}, search={search}, record_type={record_type}, payment_method={payment_method}')
        
        try:
            pm = payment_method
            if isinstance(pm, str) and pm.strip().lower() in ("", "null"):
                logger.info(f'Normalizing payment_method: "{payment_method}" -> None')
                pm = None
            else:
                logger.info(f'Payment method after normalization: {pm}')

            # Fetching more than needed to allow local filtering while maintaining pagination
            large_limit = 1000
            # We call repo with None to get all records (sales and quotes) and filter in Python
            data_all, _ = self.repository.find_all(page=1, limit=large_limit, search=search, record_type=None, payment_method=pm)
            
            # Local filtering to guarantee separation (ONLY quotes for quotations)
            filtered_data = [item for item in data_all if item.get("status") == "quote"]
            total = len(filtered_data)
            
            # Manual pagination slice
            offset = (page - 1) * limit
            data = filtered_data[offset : offset + limit]
            
            logger.info(f'After filtering ONLY "quote": {len(filtered_data)} total items, showing {len(data)} for page {page}')
            
            totalPages = math.ceil(total / limit) if limit > 0 else 0
            logger.info(f'Calculated totalPages: {totalPages}')
            
            result = {
                "data": data,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "totalPages": totalPages
                },
            }
            logger.info(f'=== QuotationUseCase.get_quotations COMPLETED SUCCESSFULLY ===')
            return result
        
        except Exception as e:
            logger.error(f'ERROR in QuotationUseCase.get_quotations: {type(e).__name__}: {str(e)}', exc_info=True)
            raise

from repositories.sale_repository import SaleRepository
class SaleUseCase:
    def __init__(self, repository : SaleRepository):
        self.repository = repository

    def get_sales(self, page=1, limit=10, search=None):
        data, total = self.repository.find_all(page, limit, search)
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
            },
        }



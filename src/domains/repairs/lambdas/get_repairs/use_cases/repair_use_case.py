
import math

from domains.repairs.lambdas.get_repairs.repositories.repair_repository import RepairRepository


class RepairUseCase:
    def __init__(self, repository : RepairRepository):
        self.repository = repository

    def get_repairs(self, page=1, limit=10, search=None):
        data, total = self.repository.find_all(page, limit, search)
        totalPages = math.ceil(total / limit )  if limit > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": totalPages
            },
        }



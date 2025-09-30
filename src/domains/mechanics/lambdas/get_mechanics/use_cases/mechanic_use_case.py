from repositories.mechanic_repository import MechanicRepository
import math
class MechanicUseCase:
    def __init__(self, repository : MechanicRepository):
        self.repository = repository

    def add_mechanic(self, mechanic):
        return self.repository.save(mechanic)

    def get_mechanics(self, page=1, limit=10, search=None):
        data, total = self.repository.find_all(page, limit, search),
        totalPages = math.ceil(total / limit )  if limit > 0 else 0
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": totalPages
            }
        }

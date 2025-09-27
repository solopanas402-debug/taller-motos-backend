from repositories.mechanic_repository import MechanicRepository
class MechanicUseCase:
    def __init__(self, repository):
        self.repository = repository

    def add_mechanic(self, mechanic):
        return self.repository.save(mechanic)

    def get_mechanics(self, page=1, limit=10, search=None):
        data, total = self.repository.find_all(page, limit, search)
        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total
            }
        }

import json
from domains.mechanics.lambdas.add_mechanic.repositories.mechanic_repository import MechanicRepository


class MechanicUseCase:
    def __init__(self, MechanicRepository  : MechanicRepository):
        self.MechanicRepository = MechanicRepository

    def add_mechanic(self, mechanic):
        return self.MechanicRepository.save(mechanic)

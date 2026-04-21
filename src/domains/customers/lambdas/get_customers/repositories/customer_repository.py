from typing import List, Tuple
from entities.customer import Customer


class CustomerRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def save(self, customer: Customer):
        data = customer.to_dict()
        response = self.db_client.table("customers").insert(data).execute()
        return response.data

    def find_all(self, page: int = 1, limit: int = 10, search: str = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit
        
        # Seleccionar columnas específicas para reducir datos transferidos
        query = self.db_client.table("customers").select(
            "id_customer, name, surname, email, id_number, phone, address, city, created_at",
            count="exact"
        )

        if search:
            search_pattern = f"%{search}%"
            # Priorizar búsqueda en campos indexados (name, email, id_number)
            # Más rápido que incluir surname en búsqueda completa
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"email.ilike.{search_pattern},"
                f"id_number.ilike.{search_pattern}"
            )
        
        response = query.limit(limit).offset(offset).execute()
        return response.data, response.count

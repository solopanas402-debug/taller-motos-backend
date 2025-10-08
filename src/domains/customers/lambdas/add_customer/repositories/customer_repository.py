from supabase import Client
from entities.customer import Customer

class CustomerRepository:
    def __init__(self, db_client : Client):
        self.db_client = db_client
    
    def save(self, customer: Customer):
        """Método para guardar un nuevo cliente en la base de datos"""
        data = customer.to_dict()
        try:
            response = self.db_client.table("customers").insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error al guardar el cliente: {str(e)}")
            return None

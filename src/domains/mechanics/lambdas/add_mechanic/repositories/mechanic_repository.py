from supabase import Client

from entities.mechanic import Mechanic


class MechanicRepository:
    def __init__(self, db_client : Client):
        self.db_client = db_client
    
    def save(self, mechanic: Mechanic):
        """Método para guardar un nuevo mecánico en la base de datos"""
        data = mechanic.to_dict()
        try:
            response = self.db_client.table("mechanics").insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error al guardar el mecánico: {str(e)}")
            return None

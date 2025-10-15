from typing import Optional, Dict, Any
from supabase import Client


class CurrentSessionRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def get_open_session_id(self) -> Optional[str]:
        """
        Obtiene el ID de la sesión de caja abierta actual
        usando la función de base de datos fn_get_open_session
        """
        try:
            response = self.db_client.rpc("fn_get_open_session").execute()
            return response.data if response.data else None
        except Exception as e:
            print(f"Error al obtener sesión abierta: {str(e)}")
            return None

    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene los detalles completos de una sesión con información de usuarios
        """
        try:
            response = self.db_client.table("cashbox_sessions").select("""
                *,
                opened_user:users!cashbox_sessions_opened_by_fkey(id_user, username, email),
                closed_user:users!cashbox_sessions_closed_by_fkey(id_user, username, email)
            """).eq("id_session", session_id).single().execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            print(f"Error al obtener detalles de sesión: {str(e)}")
            return None

    def calculate_expected_closing(self, session_id: str) -> float:
        """
        Calcula el cierre esperado actual de la sesión
        usando la función de base de datos fn_calculate_session_balance
        """
        try:
            response = self.db_client.rpc(
                "fn_calculate_session_balance",
                {"session_uuid": session_id}
            ).execute()
            
            return float(response.data) if response.data is not None else 0.0
            
        except Exception as e:
            print(f"Error al calcular balance esperado: {str(e)}")
            return 0.0

    def get_session_movements_count(self, session_id: str) -> int:
        """
        Obtiene el número de movimientos de la sesión actual
        """
        try:
            response = self.db_client.table("cashbox")\
                .select("id_cashbox", count="exact")\
                .eq("id_session", session_id)\
                .execute()
            
            return response.count if response.count else 0
            
        except Exception as e:
            print(f"Error al contar movimientos: {str(e)}")
            return 0


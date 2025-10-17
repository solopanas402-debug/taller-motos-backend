from typing import Tuple, Dict, Any, Optional
from supabase import Client


class CashboxRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str = None, 
                 session_id: str = None, date_from: str = None, 
                 date_to: str = None) -> Tuple[list[dict], int]:
        """
        Obtiene movimientos de caja usando el stored procedure get_cashboxes_cpr
        """
        offset = (page - 1) * limit
        
        try:
            # Preparar parámetros para el stored procedure
            params = {
                "p_limit": limit,
                "p_offset": offset
            }
            
            # Agregar filtros opcionales solo si tienen valor
            if search:
                params["p_search"] = search
            if session_id:
                params["p_session_id"] = session_id
            if date_from:
                params["p_date_from"] = date_from
            if date_to:
                params["p_date_to"] = date_to
            
            # Llamar al stored procedure para obtener los datos
            response = self.db_client.rpc("get_cashboxes_cpr", params).execute()
            
            if not response.data:
                return [], 0
            
            # Obtener el total con una consulta de conteo
            total = self._get_total_count(search, session_id, date_from, date_to)
            
            return response.data, total
            
        except Exception as e:
            print(f"Error al obtener movimientos de caja: {str(e)}")
            raise Exception(f"Error al consultar movimientos de caja: {str(e)}")
    
    def _get_total_count(self, search: str = None, session_id: str = None, 
                         date_from: str = None, date_to: str = None) -> int:
        """
        Obtiene el conteo total de registros aplicando los mismos filtros
        """
        try:
            query = self.db_client.table('cashbox').select('id_cashbox', count='exact')
            
            # Aplicar los mismos filtros que en la función principal
            if session_id:
                query = query.eq('id_session', session_id)
            
            if search:
                query = query.or_(f"concept.ilike.%{search}%,type.ilike.%{search}%")
            
            if date_from:
                query = query.gte('created_at', date_from)
            
            if date_to:
                query = query.lte('created_at', date_to)
            
            response = query.execute()
            return response.count if response.count is not None else 0
            
        except Exception as e:
            print(f"Error al contar registros: {str(e)}")
            return 0

    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene la sesión de caja abierta actual
        """
        try:
            response = self.db_client.rpc("fn_get_open_session").execute()
            
            if not response.data:
                return None

            session_id = response.data
            if not session_id:
                return None

            # Obtener detalles de la sesión con información de usuarios
            session_response = self.db_client.table("cashbox_sessions").select("""
                *,
                opened_user:users!cashbox_sessions_opened_by_fkey(username, email),
                closed_user:users!cashbox_sessions_closed_by_fkey(username, email)
            """).eq("id_session", session_id).single().execute()
            
            return session_response.data if session_response.data else None
            
        except Exception as e:
            print(f"Error al obtener sesión actual: {str(e)}")
            return None

    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene los detalles de una sesión específica con información de usuarios
        """
        try:
            response = self.db_client.table("cashbox_sessions").select("""
                *,
                opened_user:users!cashbox_sessions_opened_by_fkey(username, email),
                closed_user:users!cashbox_sessions_closed_by_fkey(username, email)
            """).eq("id_session", session_id).single().execute()
            
            return response.data if response.data else None
            
        except Exception as e:
            print(f"Error al obtener detalles de sesión: {str(e)}")
            return None


from typing import Dict, Any, Optional
from repositories.cashbox_repository import CashboxRepository
import math

class CashboxUseCase:
    def __init__(self, repository: CashboxRepository):
        self.repository = repository

    def get_all_cashboxes(self, page=1, limit=10, search=None, session_id=None, 
                          date_from=None, date_to=None):
        """
        Obtiene todos los movimientos de caja con paginación y filtros
        """
        data, total = self.repository.find_all(
            page=page, 
            limit=limit, 
            search=search,
            session_id=session_id,
            date_from=date_from,
            date_to=date_to
        )

        total_pages = math.ceil(total / limit) if limit > 0 and total > 0 else 0

        return {
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": total_pages
            }
        }
        
    
    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene la sesión de caja actual si está abierta
        
        Returns:
            dict con datos de la sesión o None si no hay sesión abierta
        """
        return self.repository.get_current_session()
    
    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene los detalles de una sesión específica con sus movimientos
        
        Args:
            session_id: UUID de la sesión
            
        Returns:
            dict con session (datos de sesión) y movements (lista de movimientos)
        """
        session = self.repository.get_session_details(session_id)
        if not session:
            return None
            
        # Obtener movimientos de la sesión (sin límite para traer todos)
        movements, _ = self.repository.find_all(
            page=1,
            limit=1000,  # Límite alto para obtener todos los movimientos de la sesión
            session_id=session_id
        )
        
        return {
            "session": session,
            "movements": movements
        }
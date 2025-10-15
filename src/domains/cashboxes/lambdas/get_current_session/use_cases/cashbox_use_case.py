from typing import Optional, Dict, Any
from repositories.cashbox_repository import CurrentSessionRepository


class CurrentSessionUseCase:
    def __init__(self, repository: CurrentSessionRepository):
        self.repository = repository

    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene la sesión de caja abierta actual con información completa
        
        Returns:
            dict con datos de la sesión incluyendo:
            - Datos básicos de la sesión
            - Información del usuario que abrió
            - Balance esperado actual (calculado en tiempo real)
            - Cantidad de movimientos registrados
            
            None si no hay sesión abierta
        """
        # Obtener ID de sesión abierta
        session_id = self.repository.get_open_session_id()
        
        if not session_id:
            return None
        
        # Obtener detalles de la sesión
        session = self.repository.get_session_details(session_id)
        
        if not session:
            return None
        
        # Calcular balance esperado actual
        expected_closing = self.repository.calculate_expected_closing(session_id)
        
        # Obtener cantidad de movimientos
        movements_count = self.repository.get_session_movements_count(session_id)
        
        # Agregar información calculada
        session["expected_closing_current"] = expected_closing
        session["movements_count"] = movements_count
        
        return session


from typing import Dict, Any
from repositories.dashboard_repository import DashboardRepository


class DashboardUseCase:
    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Obtiene los datos resumidos para el dashboard
        
        Returns:
            dict: Diccionario con:
                - total_products: Total de productos activos
                - pending_repairs: Reparaciones pendientes
                - monthly_sales: Ventas del mes actual
                - low_stock: Productos con stock bajo
        """
        # Obtener datos del repositorio
        summary = self.repository.get_summary()
        
        # Formatear los datos si es necesario
        return {
            "total_products": int(summary.get("total_products", 0)),
            "pending_repairs": int(summary.get("pending_repairs", 0)),
            "monthly_sales": float(summary.get("monthly_sales", 0.0)),
            "low_stock": int(summary.get("low_stock", 0))
            "lowest_stock_product_name": summary.get("lowest_stock_product_name", ""),
            "lowest_stock_product_quantity": int(summary.get("lowest_stock_product_quantity", 0))
        }


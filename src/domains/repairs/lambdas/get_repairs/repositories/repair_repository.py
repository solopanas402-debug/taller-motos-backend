from typing import List, Tuple


class RepairRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit

        query = (
            self.db_client
            .table("repairs")
            .select(
                (
                    """
                    repairs.*,
                    mechanics.name as mechanic_name,
                    mechanics.surname as mechanic_surname,
                    vehicles.brand,
                    vehicles.model,
                    vehicles.plate_number,
                    users_created.username as created_by_username,
                    users_updated.username as updated_by_username,
                    (
                        SELECT json_agg(rs.*)
                        FROM repair_services rs
                        WHERE rs.id_repair = repairs.id_repair
                    ) as services
                    """
                ),
                count="exact",
            )
            .join("mechanics", "repairs.id_mechanic", "mechanics.id_mechanic", join_type="left")
            .join("vehicles", "repairs.id_vehicle", "vehicles.id_vehicle")
            .join("users as users_created", "repairs.id_created_by", "users_created.id_user", join_type="left")
            .join("users as users_updated", "repairs.id_updated_by", "users_updated.id_user", join_type="left")
        )

        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"order_number.ilike.{search_pattern},"
                f"fault_description.ilike.{search_pattern},"
                f"diagnosis.ilike.{search_pattern},"
                f"mechanics.name.ilike.{search_pattern},"
                f"mechanics.surname.ilike.{search_pattern},"
                f"vehicles.plate_number.ilike.{search_pattern}"
            )

        response = query.range(offset, offset + limit - 1).execute()
        return response.data or [], response.count or 0



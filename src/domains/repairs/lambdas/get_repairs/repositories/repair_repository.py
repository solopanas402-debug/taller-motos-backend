from typing import List, Tuple

from db.db_client import DBClient


class RepairRepository:
    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None) -> Tuple[List[dict], int]:
        offset = (page - 1) * limit

        # 1) Traer repairs paginados (sin joins)
        repairs_query = self.db_client.table("repairs").select("*", count="exact")

        if search:
            search_pattern = f"%{search}%"
            repairs_query = repairs_query.or_(
                f"order_number.ilike.{search_pattern},"
                f"fault_description.ilike.{search_pattern},"
                f"diagnosis.ilike.{search_pattern}"
            )

        repairs_resp = repairs_query.range(offset, offset + limit - 1).execute()
        repairs = repairs_resp.data or []
        total = repairs_resp.count or 0

        if not repairs:
            return [], total

        # 2) Resolver referencias en lote
        id_mechanics = list({r.get("id_mechanic") for r in repairs if r.get("id_mechanic")})
        id_vehicles = list({r.get("id_vehicle") for r in repairs if r.get("id_vehicle")})
        id_created_by = list({r.get("id_created_by") for r in repairs if r.get("id_created_by")})
        id_updated_by = list({r.get("id_updated_by") for r in repairs if r.get("id_updated_by")})
        id_repairs = [r.get("id_repair") for r in repairs if r.get("id_repair")]

        mechanics_map: dict = {}
        vehicles_map: dict = {}
        users_map: dict = {}
        services_map: dict = {rid: [] for rid in id_repairs}

        if id_mechanics:
            m_resp = (
                self.db_client.table("mechanics")
                .select("id_mechanic,name,surname")
                .in_("id_mechanic", id_mechanics)
                .execute()
            )
            for m in (m_resp.data or []):
                mechanics_map[m["id_mechanic"]] = m

        if id_vehicles:
            v_resp = (
                self.db_client.table("vehicles")
                .select("id_vehicle,brand,model,plate_number")
                .in_("id_vehicle", id_vehicles)
                .execute()
            )
            for v in (v_resp.data or []):
                vehicles_map[v["id_vehicle"]] = v

        user_ids = list(set(id_created_by + id_updated_by)) if (id_created_by or id_updated_by) else []
        if user_ids:
            u_resp = (
                self.db_client.table("users")
                .select("id_user,username")
                .in_("id_user", user_ids)
                .execute()
            )
            for u in (u_resp.data or []):
                users_map[u["id_user"]] = u

        if id_repairs:
            s_resp = (
                self.db_client.table("repair_services")
                .select("*")
                .in_("id_repair", id_repairs)
                .execute()
            )
            for s in (s_resp.data or []):
                rid = s.get("id_repair")
                if rid in services_map:
                    services_map[rid].append(s)
                else:
                    services_map[rid] = [s]

        # 3) Enriquecer cada repair con datos relacionados
        enriched: List[dict] = []
        for r in repairs:
            id_mech = r.get("id_mechanic")
            id_veh = r.get("id_vehicle")
            id_cb = r.get("id_created_by")
            id_ub = r.get("id_updated_by")
            rid = r.get("id_repair")

            mechanic = mechanics_map.get(id_mech) if id_mech else None
            vehicle = vehicles_map.get(id_veh) if id_veh else None
            created_by = users_map.get(id_cb) if id_cb else None
            updated_by = users_map.get(id_ub) if id_ub else None

            enriched.append({
                **r,
                "mechanic_name": mechanic.get("name") if mechanic else None,
                "mechanic_surname": mechanic.get("surname") if mechanic else None,
                "brand": vehicle.get("brand") if vehicle else None,
                "model": vehicle.get("model") if vehicle else None,
                "plate_number": vehicle.get("plate_number") if vehicle else None,
                "created_by_username": created_by.get("username") if created_by else None,
                "updated_by_username": updated_by.get("username") if updated_by else None,
                "services": services_map.get(rid, []),
            })

        return enriched, total



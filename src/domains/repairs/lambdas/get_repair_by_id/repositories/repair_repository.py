from supabase import Client


class RepairRepository:
    def __init__(self, db_client: Client):
        self.db_client = db_client

    def find_by_id(self, id_repair: str):
        """
        Busca una reparacion por ID con sus materiales y servicio.
        """
        try:
            # Get repair base data
            response = self.db_client.table("repairs") \
                .select("*") \
                .eq('id_repair', id_repair) \
                .limit(1) \
                .execute()

            if not response.data:
                return None

            repair = response.data[0]

            # Get vehicle + customer
            if repair.get('id_vehicle'):
                vehicle_resp = self.db_client.table("vehicles") \
                    .select("license_plate, brand, model, year, id_customer") \
                    .eq('id_vehicle', repair['id_vehicle']) \
                    .limit(1) \
                    .execute()
                if vehicle_resp.data:
                    v = vehicle_resp.data[0]
                    repair['vehicle_brand'] = v.get('brand', '')
                    repair['vehicle_model'] = v.get('model', '')
                    repair['license_plate'] = v.get('license_plate', '')

                    # Get customer
                    if v.get('id_customer'):
                        customer_resp = self.db_client.table("customers") \
                            .select("name, surname, id_number, phone") \
                            .eq('id_customer', v['id_customer']) \
                            .limit(1) \
                            .execute()
                        if customer_resp.data:
                            c = customer_resp.data[0]
                            repair['customer_full_name'] = f"{c.get('name', '')} {c.get('surname', '')}".strip()
                            repair['customer_id_number'] = c.get('id_number', 'N/A')
                            repair['customer_phone'] = c.get('phone', 'No disponible')

            # Get mechanic
            if repair.get('id_mechanic'):
                mechanic_resp = self.db_client.table("mechanics") \
                    .select("name, surname") \
                    .eq('id_mechanic', repair['id_mechanic']) \
                    .limit(1) \
                    .execute()
                if mechanic_resp.data:
                    m = mechanic_resp.data[0]
                    repair['mechanic_full_name'] = f"{m.get('name', '')} {m.get('surname', '')}".strip()

            # Get materials with product names
            materials_resp = self.db_client.table("repair_materials") \
                .select("id_product, quantity, unit_price, discount, subtotal") \
                .eq('id_repair', id_repair) \
                .execute()

            if materials_resp.data:
                product_ids = [m['id_product'] for m in materials_resp.data]
                products_resp = self.db_client.table("products") \
                    .select("id_product, name") \
                    .in_('id_product', product_ids) \
                    .execute()
                product_names = {p['id_product']: p['name'] for p in (products_resp.data or [])}

                repair['products'] = [
                    {
                        'id_product': m['id_product'],
                        'name': product_names.get(m['id_product'], m['id_product']),
                        'quantity': m.get('quantity', 0),
                        'unit_price': float(m.get('unit_price', 0)),
                        'discount': float(m.get('discount', 0)),
                        'subtotal': float(m.get('subtotal', 0)),
                    }
                    for m in materials_resp.data
                ]
            else:
                repair['products'] = []

            # Get labor/service
            services_resp = self.db_client.table("repair_services") \
                .select("agreed_price, id_service_type") \
                .eq('id_repair', id_repair) \
                .limit(1) \
                .execute()

            if services_resp.data:
                s = services_resp.data[0]
                repair['labor'] = {
                    'agreed_price': float(s.get('agreed_price', 0)),
                    'id_service_type': s.get('id_service_type', ''),
                }

            return repair
        except Exception as e:
            print(f"Error al buscar la reparación: {str(e)}")
            raise Exception(f'Ha ocurrido un problema al buscar el reparación: {str(e)}')

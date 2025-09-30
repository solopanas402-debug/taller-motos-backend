from entities.product import Product


class ProductRepository:
    def __init__(self, db_client):
        self.db_client = db_client

    def find_all(self, page: int = 1, limit: int = 10, search: str | None = None):
        offset = (page - 1) * limit
        query = self.db_client.table("products").select("*", count="exact")
        if search:
            search_pattern = f"%{search}%"
            query = query.or_(
                f"name.ilike.{search_pattern},"
                f"description.ilike.{search_pattern},"
                f"code.ilike.{search_pattern}"
            )
        response = query.range(offset, offset + limit - 1).execute()
        return (response.data or [], response.count or 0)

    # def find_all(self):
    #     try:
    #         response = self.db_client.table("products").select("*").execute()
    #
    #         if not response:
    #             return None
    #
    #         products = response.data
    #
    #         print(f'productos recuperados en repository: {products}')
    #
    #         # return [Product.from_dict(row) for row in products]
    #
    #         return products
    #     except Exception as e:
    #         raise Exception(f"Error al obtener los productos: {e}")

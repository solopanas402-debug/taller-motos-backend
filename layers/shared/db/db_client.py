import requests
import json
from config.config import Config


class DBClient:
    _client = None
    
    @staticmethod
    def get_client():
        """Retorna un cliente que usa requests directamente en lugar del SDK"""
        if DBClient._client is None:
            DBClient._client = SupabaseRestClient(Config.DB_URL, Config.DB_KEY)
        return DBClient._client


class SupabaseRestClient:
    """Cliente REST para Supabase que no requiere validación de API key"""
    
    def __init__(self, url, key):
        self.url = url
        self.key = key
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def table(self, table_name):
        """Retorna un objeto para hacer queries a una tabla"""
        return SupabaseTable(self.url, self.headers, table_name)
    
    def rpc(self, function_name, params=None):
        """Llama a una función RPC de Supabase"""
        return SupabaseRPC(self.url, self.headers, function_name, params)


class SupabaseTable:
    """Representa una tabla en Supabase"""
    
    def __init__(self, base_url, headers, table_name):
        self.base_url = base_url
        self.headers = headers
        self.table_name = table_name
        self.url = f"{base_url}/rest/v1/{table_name}"
    
    def select(self, *args, count=None):
        """SELECT query"""
        query = SupabaseQuery(self.url, self.headers, "GET")
        if count:
            query._count = count
        return query
    
    def insert(self, data):
        """INSERT query"""
        query = SupabaseQuery(self.url, self.headers, "POST")
        query.data = data
        return query
    
    def update(self, data):
        """UPDATE query"""
        query = SupabaseQuery(self.url, self.headers, "PATCH")
        query.data = data
        return query
    
    def delete(self):
        """DELETE query"""
        return SupabaseQuery(self.url, self.headers, "DELETE")


class SupabaseQuery:
    """Representa una query a Supabase"""
    
    def __init__(self, url, headers, method):
        self.url = url
        self.headers = headers
        self.method = method
        self.data = None
        self.filters = []
        self._limit = None
        self._offset = None
        self._order = None
        self._count = None
    
    def eq(self, column, value):
        """Filtro de igualdad"""
        self.filters.append(f"{column}=eq.{value}")
        return self
    
    def neq(self, column, value):
        """Filtro de desigualdad"""
        self.filters.append(f"{column}=neq.{value}")
        return self
    
    def gt(self, column, value):
        """Filtro mayor que"""
        self.filters.append(f"{column}=gt.{value}")
        return self
    
    def gte(self, column, value):
        """Filtro mayor o igual que"""
        self.filters.append(f"{column}=gte.{value}")
        return self
    
    def lt(self, column, value):
        """Filtro menor que"""
        self.filters.append(f"{column}=lt.{value}")
        return self
    
    def lte(self, column, value):
        """Filtro menor o igual que"""
        self.filters.append(f"{column}=lte.{value}")
        return self
    
    def like(self, column, pattern):
        """Filtro LIKE"""
        self.filters.append(f"{column}=like.{pattern}")
        return self
    
    def ilike(self, column, pattern):
        """Filtro ILIKE (case insensitive)"""
        self.filters.append(f"{column}=ilike.{pattern}")
        return self
    
    def is_(self, column, value):
        """Filtro IS (para null, true, false)"""
        self.filters.append(f"{column}=is.{value}")
        return self
    
    def in_(self, column, values):
        """Filtro IN"""
        if isinstance(values, (list, tuple)):
            values_str = ",".join(str(v) for v in values)
            self.filters.append(f"{column}=in.({values_str})")
        return self
    
    def or_(self, conditions):
        """Filtro OR"""
        self.filters.append(f"or=({conditions})")
        return self
    
    def limit(self, count):
        """Limita el número de resultados"""
        self._limit = count
        return self
    
    def offset(self, count):
        """Salta los primeros N resultados"""
        self._offset = count
        return self
    
    def order(self, column, desc=False):
        """Ordena los resultados"""
        direction = "desc" if desc else "asc"
        self._order = f"{column}.{direction}"
        return self
    
    def execute(self):
        """Ejecuta la query"""
        try:
            # Construir query string
            params = []
            
            if self.filters:
                params.extend(self.filters)
            
            if self._limit is not None:
                params.append(f"limit={self._limit}")
            
            if self._offset is not None:
                params.append(f"offset={self._offset}")
            
            if self._order:
                params.append(f"order={self._order}")
            
            # Construir URL
            if params:
                query_string = "&".join(params)
                url = f"{self.url}?{query_string}"
            else:
                url = self.url
            
            # Agregar header para count si se solicita
            headers = self.headers.copy()
            if self._count:
                headers["Prefer"] = f"count={self._count}"
            
            # Ejecutar request
            if self.method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif self.method == "POST":
                response = requests.post(url, json=self.data, headers=headers, timeout=10)
            elif self.method == "PATCH":
                response = requests.patch(url, json=self.data, headers=headers, timeout=10)
            elif self.method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            
            if response.status_code < 400:
                result = response.json() if response.text else []
                
                # Si se solicitó count, agregarlo al resultado
                if self._count and 'content-range' in response.headers:
                    content_range = response.headers['content-range']
                    # Format: "0-9/total" o "*/total"
                    if '/' in content_range:
                        total = int(content_range.split('/')[-1])
                        # Crear objeto similar a la respuesta de Supabase
                        class QueryResponse:
                            def __init__(self, data, count):
                                self.data = data
                                self.count = count
                        return QueryResponse(result, total)
                
                # Retornar objeto con data para compatibilidad
                class QueryResponse:
                    def __init__(self, data):
                        self.data = data
                        self.count = None
                return QueryResponse(result)
            else:
                print(f"Error Supabase: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en query: {e}")
            import traceback
            traceback.print_exc()
            return None



class SupabaseRPC:
    """Representa una llamada RPC a Supabase"""
    
    def __init__(self, base_url, headers, function_name, params=None):
        self.base_url = base_url
        self.headers = headers
        self.function_name = function_name
        self.params = params or {}
        self.url = f"{base_url}/rest/v1/rpc/{function_name}"
    
    def execute(self):
        """Ejecuta la llamada RPC"""
        try:
            response = requests.post(
                self.url, 
                json=self.params, 
                headers=self.headers, 
                timeout=10
            )
            
            if response.status_code < 400:
                result = response.json() if response.text else []
                
                # Retornar objeto con data para compatibilidad
                class RPCResponse:
                    def __init__(self, data):
                        self.data = data
                        self.count = None
                return RPCResponse(result)
            else:
                print(f"Error RPC Supabase: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en RPC: {e}")
            import traceback
            traceback.print_exc()
            return None

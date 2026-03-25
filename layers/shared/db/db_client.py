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


class SupabaseTable:
    """Representa una tabla en Supabase"""
    
    def __init__(self, base_url, headers, table_name):
        self.base_url = base_url
        self.headers = headers
        self.table_name = table_name
        self.url = f"{base_url}/rest/v1/{table_name}"
    
    def select(self, *args):
        """SELECT query"""
        return SupabaseQuery(self.url, self.headers, "GET")
    
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
    
    def eq(self, column, value):
        """Filtro de igualdad"""
        self.filters.append(f"{column}=eq.{value}")
        return self
    
    def execute(self):
        """Ejecuta la query"""
        try:
            if self.filters:
                query_string = "&".join(self.filters)
                url = f"{self.url}?{query_string}"
            else:
                url = self.url
            
            if self.method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif self.method == "POST":
                response = requests.post(url, json=self.data, headers=self.headers, timeout=10)
            elif self.method == "PATCH":
                response = requests.patch(url, json=self.data, headers=self.headers, timeout=10)
            elif self.method == "DELETE":
                response = requests.delete(url, headers=self.headers, timeout=10)
            
            if response.status_code < 400:
                return response.json() if response.text else []
            else:
                print(f"Error Supabase: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en query: {e}")
            return None


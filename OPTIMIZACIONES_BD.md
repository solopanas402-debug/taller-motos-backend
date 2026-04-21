# Optimizaciones de Base de Datos - Taller Motos Backend

## Problemas Identificados

### 1. **PRODUCTS - get_products** ⚠️ CRÍTICO
**Problema**: Se ejecutan 2 SQLs separados (uno para datos, otro para count)
```python
# ❌ ACTUAL (Ineficiente)
response = query.limit(limit).offset(offset).execute()
count_query = self.db_client.table("products").select("*", count="exact")
count_response = count_query.execute()  # Segunda query innecesaria
```

**Solución**: Usar `count` en la misma query
```python
# ✅ OPTIMIZADO
query = self.db_client.table("products").select("*", count="exact")
response = query.limit(limit).offset(offset).execute()
total = response.count  # No segunda query
```

### 2. **CUSTOMERS - get_customers** ⚠️ ALTO IMPACTO
**Problema**: Búsqueda ILIKE sin columnas indexadas
```python
# ❌ ACTUAL
query.or_(f"name.ilike.{search_pattern},surname.ilike.{search_pattern},...")
```

**Solución**: Usar índices y búsqueda específica
- Crear índice en `customers(name, email)` en BD
- Priorizar búsqueda en campos indexados
- Usar `fulltext` search si está disponible en Supabase

### 3. **SALES - get_sales** ⚠️ MEDIO
**Problema**: RPC con muchos parámetros NULL, sin caching
**Solución**: 
- Usar campos selectivos en RPC
- Implementar query builder condicional
- Cachear resultados frecuentes

### 4. **SELECTS SIN COLUMNAS ESPECÍFICAS** ⚠️ TODOS LOS DOMINIOS
**Problema**: Todas las queries hacen `SELECT "*"`
```python
# ❌ ACTUAL
.select("*")

# ✅ OPTIMIZADO - Ejemplo Products
.select("id_product, name, code, price, stock, category_id")
```

**Impacto**: Reduce ancho de banda, mejora velocidad de transferencia

### 5. **N+1 QUERIES en add_sale**
**Problema**: Al guardar venta se hacen múltiples queries relacionadas
**Solución**: Usar RPC o transacciones para una sola llamada

---

## Recomendaciones por Dominio

### PRODUCTS
- [ ] Usar `count` en la misma query
- [ ] Seleccionar columnas específicas
- [ ] Crear índices: `idx_products_name`, `idx_products_code`
- [ ] Implementar validación client-side de paginación

### CUSTOMERS
- [ ] Crear índice: `idx_customers_name_email`
- [ ] Usar búsqueda en campos indexados first
- [ ] Validar límite máximo de búsqueda (evitar LIKE "%texto%")
- [ ] Implementar caching en customer frecuentes

### SALES
- [ ] Revisar RPC `get_sales_cpr` - verificar índices en BD
- [ ] Usar selects específicas en related data
- [ ] Implementar cache de 5-10 minutos para listados
- [ ] Usar connection pooling en production

### GENERAL
- [ ] Añadir índices faltantes en todas las tablas
- [ ] Implementar timeouts en queries (10s máximo)
- [ ] Usar batch operations para inserts múltiples
- [ ] Monitorear slow queries en Supabase dashboard

---

## Cambios a Implementar

1. ✅ Optimizar `get_products` - eliminar segunda query
2. ✅ Selecciones específicas en todas las queries
3. ✅ Mejorar búsquedas en customers
4. ✅ Añadir límites a queries sin límite
5. ✅ Implementar índices recomendados


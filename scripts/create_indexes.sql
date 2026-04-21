-- Optimización de Índices - Taller Motos Backend
-- Script SQL para ejecutar en Supabase

-- ===================================
-- PRODUCTS - Índices para búsqueda
-- ===================================
CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);
CREATE INDEX IF NOT EXISTS idx_products_code ON products(code);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_name_code ON products(name, code);

-- ===================================
-- CUSTOMERS - Índices para búsqueda
-- ===================================
CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name);
CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email);
CREATE INDEX IF NOT EXISTS idx_customers_id_number ON customers(id_number);
CREATE INDEX IF NOT EXISTS idx_customers_name_email ON customers(name, email);

-- ===================================
-- SALES - Índices para búsqueda
-- ===================================
CREATE INDEX IF NOT EXISTS idx_sales_id_customer ON sales(id_customer);
CREATE INDEX IF NOT EXISTS idx_sales_status ON sales(status);
CREATE INDEX IF NOT EXISTS idx_sales_created_at ON sales(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_sales_payment_method ON sales(payment_method);

-- ===================================
-- SALE_DETAILS - Índices para queries relacionadas
-- ===================================
CREATE INDEX IF NOT EXISTS idx_sale_details_id_sale ON sale_details(id_sale);
CREATE INDEX IF NOT EXISTS idx_sale_details_id_product ON sale_details(id_product);

-- ===================================
-- Estadísticas (ANALYZE para optimizador)
-- ===================================
ANALYZE products;
ANALYZE customers;
ANALYZE sales;
ANALYZE sale_details;

-- ===================================
-- Validar índices creados
-- ===================================
-- Ejecutar para ver índices creados:
-- SELECT * FROM pg_indexes WHERE schemaname = 'public' ORDER BY tablename, indexname;

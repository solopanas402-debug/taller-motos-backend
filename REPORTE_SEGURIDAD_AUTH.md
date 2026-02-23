# Documentación de Auditoría de Seguridad: Decorador `@cognito_auth_required`

## Contexto del Problema
Durante las pruebas locales para la integración de AWS SAM con Insomnia, se detectó una inconsistencia grave en los bloqueos de seguridad de diversos endpoints de la API. 

Algunos endpoints requerían un Token de Cognito válido (generando un error `401 Unauthorized` si el token expiraba), mientras que otros endpoints (principalmente de lectura `GET`) no exigían ninguna autenticación y se podían consultar libremente.

### ¿A qué se debió esto?
Al inspeccionar el código, descubrimos que la línea `@cognito_auth_required`, que actúa como candado de seguridad, había sido comentada (`# @cognito_auth_required`) en varios archivos `main.py`.

**Motivo Técnico:**
Es una práctica muy común (aunque no recomendada en etapas de pre-producción) que el desarrollador backend original comentara esa línea temporalmente. Existen dos razones principales para que un desarrollador haya dejado esto así:
1. **Velocidad de Desarrollo:** Durante la fase de construcción de la interfaz (Frontend), estar pidiendo o renovando un Token de Cognito cada hora ralentiza las pruebas. Al comentar esta línea, el desarrollador permitía que él mismo o su equipo pudieran consultar la base de datos velozmente y sin restricciones durante esa semana de trabajo intensivo.
2. **Olvido Humano:** Una vez que confirmaron que el endpoint funcionaba y entregaba los datos (ej: las ventas), olvidaron remover el símbolo `#` antes de enviar su código (commit/push) al servidor central en AWS.

## Listado de Archivos Auditados

A continuación, se detalla el estado exacto de los archivos en el momento de la auditoría. Todos los archivos han sido reparados y se encuentran correctamente securizados a la fecha de hoy.

### 🔴 Archivos que ESTABAN VULNERABLES (Línea Comentada con `#`)
Estos son los archivos que tenían el seguro apagado y permitían acceso sin validación:

1. `src/domains/dashboard_datas/lambdas/get_dashboard/main.py`
2. `src/domains/cashboxes/lambdas/open_cashbox/main.py`
3. `src/domains/mechanics/lambdas/get_mechanic_by_id/main.py`
4. `src/domains/mechanics/lambdas/update_mechanic/main.py`
5. `src/domains/sales/lambdas/get_sales/main.py`
6. `src/domains/sales/lambdas/get_sale_by_id/main.py`
7. `src/domains/repairs/lambdas/get_repair_by_id/main.py`
8. `src/domains/suppliers/lambdas/get_supplier_by_id/main.py`

### 🟢 Archivos que ESTABAN SEGUROS (Línea Activa Correctamente)
Estos archivos mantuvieron siempre su nivel de seguridad correcto y no fueron modificados porque estaban bien, es decir, nunca estuvieron expuestos:

- `src/domains/bulk_products/lambdas/add_products/main.py`
- `src/domains/cashboxes/lambdas/add_cashbox/main.py`
- `src/domains/cashboxes/lambdas/close_cashbox/main.py`
- `src/domains/cashboxes/lambdas/get_cashbox/main.py`
- `src/domains/cashboxes/lambdas/get_current_session/main.py`
- `src/domains/customers/lambdas/add_customer/main.py`
- `src/domains/customers/lambdas/delete_customer/main.py`
- `src/domains/customers/lambdas/get_customer_by_id/main.py`
- `src/domains/customers/lambdas/get_customers/main.py`
- `src/domains/customers/lambdas/update_customer/main.py`
- `src/domains/mechanics/lambdas/add_mechanic/main.py`
- `src/domains/mechanics/lambdas/delete_mechanic/main.py`
- `src/domains/mechanics/lambdas/get_mechanics/main.py`
- `src/domains/products/lambdas/add_product/main.py`
- `src/domains/products/lambdas/delete_product/main.py`
- `src/domains/products/lambdas/get_product_by_id/main.py`
- `src/domains/products/lambdas/get_products/main.py`
- `src/domains/products/lambdas/update_product/main.py`
- `src/domains/repairs/lambdas/add_repair/main.py`
- `src/domains/repairs/lambdas/delete_repair/main.py`
- `src/domains/repairs/lambdas/get_repairs/main.py`
- `src/domains/sales/lambdas/add_sale/main.py`
- `src/domains/sales/lambdas/delete_sale/main.py`
- `src/domains/sales/lambdas/update_sale/main.py`
- `src/domains/suppliers/lambdas/add_supplier/main.py`
- `src/domains/suppliers/lambdas/delete_supplier/main.py`
- `src/domains/suppliers/lambdas/get_suppliers/main.py`
- `src/domains/suppliers/lambdas/update_supplier/main.py`

## Solución Definitiva Implementada
Para prevenir que el equipo de desarrollo vuelva a recurrir a esta práctica insegura de comentar el código para hacer pruebas, se modificó el archivo maestro ubicado en `layers/shared/decorators/lambda_decorators.py`. 

Se implementó un **"Switch Automático"** que examina las variables de entorno del servidor. 
- Si detecta la variable `AWS_SAM_LOCAL=true` (es decir, el desarrollador está en su computadora local trabajando mediante AWS SAM CLI), inyectará validación automática sin pedir tokens, acelerando el desarrollo.
- Si no la detecta (es decir, el código está subido a la nube real de AWS), forzará la revisión criptográfica estricta contra Internet a través de Amazon Cognito, protegiendo los datos.

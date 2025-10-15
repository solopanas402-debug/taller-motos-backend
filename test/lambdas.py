import importlib

LAMBDA_MODULES = {
    "add_customer": "src.domains.customers.lambdas.add_customer.main",
    "get_customers": "src.domains.customers.lambdas.get_customers.main",
    "get_customer_by_id": "src.domains.customers.lambdas.get_customer_by_id.main",
    "delete_customer": "src.domains.customers.lambdas.delete_customer.main",
    "update_customer": "src.domains.customers.lambdas.update_customer.main",
    "add_mechanic": "src.domains.mechanics.lambdas.add_mechanic.main",
    "get_mechanics": "src.domains.mechanics.lambdas.get_mechanics.main",
    "get_mechanic_by_id": "src.domains.mechanics.lambdas.get_mechanic_by_id.main",
    "delete_mechanic": "src.domains.mechanics.lambdas.delete_mechanic.main",
    "update_mechanic": "src.domains.mechanics.lambdas.update_mechanic.main",
    "add_product": "src.domains.products.lambdas.add_product.main",
    "get_product_by_id": "src.domains.products.lambdas.get_product_by_id.main",
    "get_products": "src.domains.products.lambdas.get_products.main",
    "delete_product": "src.domains.products.lambdas.delete_product.main",
    "update_product": "src.domains.products.lambdas.update_product.main",
    "add_products": "src.domains.bulk_products.lambdas.add_products.main",
    "add_repair": "src.domains.repairs.lambdas.add_repair.main",
    "get_repairs": "src.domains.repairs.lambdas.get_repairs.main",
    "get_repair_by_id": "src.domains.repairs.lambdas.get_repair_by_id.main",
    "add_sale": "src.domains.sales.lambdas.add_sale.main",
    "get_sales": "src.domains.sales.lambdas.get_sales.main",
    "get_sale_by_id": "src.domains.sales.lambdas.get_sale_by_id.main",
    "delete_sale": "src.domains.sales.lambdas.delete_sale.main",
    "update_sale": "src.domains.sales.lambdas.update_sale.main",
    "add_supplier": "src.domains.suppliers.lambdas.add_supplier.main",
    "get_suppliers": "src.domains.suppliers.lambdas.get_suppliers.main",
    "get_supplier_by_id": "src.domains.suppliers.lambdas.get_supplier_by_id.main",
    "delete_supplier": "src.domains.suppliers.lambdas.delete_supplier.main",
    "update_supplier": "src.domains.suppliers.lambdas.update_supplier.main",
    # Cashbox lambdas
    "get_cashbox": "src.domains.cashboxes.lambdas.get_cashbox.main",
    "add_cashbox": "src.domains.cashboxes.lambdas.add_cashbox.main",
    "open_cashbox": "src.domains.cashboxes.lambdas.open_cashbox.main",
    "close_cashbox": "src.domains.cashboxes.lambdas.close_cashbox.main",
    "get_current_session": "src.domains.cashboxes.lambdas.get_current_session.main",
    # Dashboard lambdas
    "get_dashboard": "src.domains.dashboard_datas.lambdas.get_dashboard.main",
}


def get_lambda(name):
    if name not in LAMBDA_MODULES:
        raise ValueError(f"Lambda '{name}' no encontrada")

    module_path = LAMBDA_MODULES[name]
    module = importlib.import_module(module_path)
    return module.lambda_handler

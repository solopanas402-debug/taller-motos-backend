import importlib

LAMBDA_MODULES = {
    "add_customer": "src.domains.customers.lambdas.add_customer.main",
    "get_customers": "src.domains.customers.lambdas.get_customers.main",
    "add_mechanic": "src.domains.mechanics.lambdas.add_mechanic.main",
    "get_mechanics": "src.domains.mechanics.lambdas.get_mechanics.main",
    "add_product": "src.domains.products.lambdas.add_product.main",
    "get_product_by_id": "src.domains.products.lambdas.get_product_by_id.main",
    "get_products": "src.domains.products.lambdas.get_products.main",
    "add_supplier": "src.domains.suppliers.lambdas.add_supplier.main",
    "get_suppliers": "src.domains.suppliers.lambdas.get_suppliers.main",
    "add_sale": "src.domains.sales.lambdas.add_sale.main",
    # "add_mechanic": "src.domains.mechanics.lambdas.add_mechanic.main",
    # "get_mechanics": "src.domains.mechanics.lambdas.get_mechanics.main",
}


def get_lambda(name):
    if name not in LAMBDA_MODULES:
        raise ValueError(f"Lambda '{name}' no encontrada")

    module_path = LAMBDA_MODULES[name]
    module = importlib.import_module(module_path)
    return module.lambda_handler

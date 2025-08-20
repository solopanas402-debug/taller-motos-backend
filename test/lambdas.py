from src.domains.customers.lambdas.add_customer import main as add_customers_handler
from src.domains.customers.lambdas.get_customers import main as get_customers_handler
from src.domains.mechanics.lambdas.add_mechanic import main as add_mechanic_handler
from src.domains.mechanics.lambdas.get_mechanics import main as get_mechanics_handler
from src.domains.products.lambdas.add_product import main as add_product_handler
from src.domains.products.lambdas.get_products import main as get_products_handler
from src.domains.products.lambdas.get_product_by_id import main as get_product_handler
from src.domains.suppliers.lambdas.add_supplier import main as add_supplier_handler
from src.domains.suppliers.lambdas.get_suppliers import main as get_suppliers_handler

lambdas = {
    "add_customer": add_customers_handler.lambda_handler,
    "get_customers": get_customers_handler.lambda_handler,
    "add_mechanic": add_mechanic_handler.lambda_handler,
    "get_mechanics": get_mechanics_handler.lambda_handler,
    "add_product": add_product_handler.lambda_handler,
    "get_product_by_id": get_product_handler.lambda_handler,
    "get_products": get_products_handler.lambda_handler,
    "add_supplier": add_supplier_handler.lambda_handler,
    "get_suppliers": get_suppliers_handler.lambda_handler,
}

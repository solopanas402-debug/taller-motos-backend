from src.customers import handler as customers_handler
from src.mechanics import handler as mechanics_handler
from src.products import handler as products_handler
from src.providers import handler as providers_handler

lambdas = {
    "customers_get": customers_handler.lambda_handler,
    "mechanics_get": mechanics_handler.lambda_handler,
    "products_get": products_handler.lambda_handler,
    "providers_get": providers_handler.lambda_handler,

}
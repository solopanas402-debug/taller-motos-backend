import json
from repositories.customer_repository import CustomerRepository


class CustomerUseCase:
    def __init__(self, CustomerRepository  : CustomerRepository):
        self.CustomerRepository = CustomerRepository

    def add_customer(self, customer):
        return self.CustomerRepository.save(customer)
